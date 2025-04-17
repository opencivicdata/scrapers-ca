import csv
import os
import re
from collections import defaultdict
from datetime import datetime
from ftplib import FTP
from io import BytesIO, StringIO
from urllib.parse import unquote, urlparse
from zipfile import ZipFile

import agate
import agateexcel  # noqa: F401
import cloudscraper
import lxml.html
import requests
from lxml import etree
from opencivicdata.divisions import Division
from pupa.scrape import Jurisdiction, Organization, Person, Post, Scraper
from requests.packages.urllib3.exceptions import InsecureRequestWarning

import patch  # patch patches validictory # noqa: F401

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

CUSTOM_USER_AGENT = "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)"
DEFAULT_USER_AGENT = requests.utils.default_user_agent()
SCRAPER = cloudscraper.create_scraper()

CONTACT_DETAIL_TYPE_MAP = {
    "Address": "address",
    "bb": "cell",  # BlackBerry
    "bus": "voice",
    "Bus": "voice",
    "Bus.": "voice",
    "Business": "voice",
    "Cell": "cell",
    "Cell Phone": "cell",
    "City Hall": "voice",
    "Email": "email",
    "Fax": "fax",
    "Home": "voice",
    "Home Phone": "voice",
    "Home Phone*": "voice",
    "Office": "voice",
    "ph": "voice",
    "Phone": "voice",
    "Res": "voice",
    "Res/Bus": "voice",
    "Residence": "voice",
    "Téléphone (maison)": "voice",
    "Téléphone (bureau)": "voice",
    "Téléphone (cellulaire)": "cell",
    "Téléphone (résidence)": "voice",
    "Téléphone (résidence et bureau)": "voice",
    "Voice Mail": "voice",
    "Work": "voice",
}
# In Newmarket, for example, there are both "Phone" and "Business" numbers.
CONTACT_DETAIL_NOTE_MAP = {
    "Address": "legislature",
    "bb": "legislature",
    "bus": "office",
    "Bus": "office",
    "Bus.": "office",
    "Business": "office",
    "Cell": "legislature",
    "Cell Phone": "legislature",
    "City Hall": "office",
    "Email": None,
    "Fax": "legislature",
    "Home": "residence",
    "Home Phone": "residence",
    "Home Phone*": "residence",
    "ph": "legislature",
    "Phone": "legislature",
    "Office": "legislature",
    "Res": "residence",
    "Res/Bus": "office",
    "Residence": "residence",
    "Téléphone (maison)": "residence",
    "Téléphone (bureau)": "legislature",
    "Téléphone (cellulaire)": "legislature",
    "Téléphone (résidence)": "residence",
    "Téléphone (résidence et bureau)": "legislature",
    "Voice Mail": "legislature",
    "Work": "legislature",
}
SSL_VERIFY = "/usr/lib/ssl/certs/ca-certificates.crt" if os.getenv("SSL_VERIFY", "") else True

email_re = re.compile(r"([A-Za-z0-9._-]+@(?:[A-Za-z0-9-]+\.)+[A-Za-z]{2,})")


styles_of_address = {}
for gid in range(3):
    response = requests.get(
        f"https://docs.google.com/spreadsheets/d/11qUKd5bHeG5KIzXYERtVgs3hKcd9yuZlt-tCTLBFRpI/pub?single=true&gid={gid}&output=csv",
        verify=SSL_VERIFY,
    )
    if response.status_code == 200:
        response.encoding = "utf-8"
        for row in csv.DictReader(StringIO(response.text)):
            identifier = row.pop("Identifier")
            for field in list(row.keys()):
                if not row[field] or field == "Name":
                    row.pop(field)
            if row:
                styles_of_address[identifier] = row


class CanadianScraper(Scraper):
    def get_email(self, node, expression=".", *, error=True):
        """
        Make sure that the node/expression is narrow enough to not capture a
        generic email address in the footer of the page, for example.
        """
        # If the text would be split across multiple sub-tags.
        matches = [match.text_content() for match in node.xpath(f'{expression}//*[contains(text(), "@")]')]
        # The text version is more likely to be correct, as it is more visible,
        # e.g. ca_bc has one `href` of `mailto:first.last.mla@leg.bc.ca`.
        matches.extend(
            unquote(match.attrib["href"]) for match in node.xpath(f'{expression}//a[contains(@href, "mailto:")]')
        )
        # Some emails are obfuscated by Cloudflare.
        matches.extend(
            self._cloudflare_decode(match)
            for match in node.xpath(f'{expression}//@href[contains(., "cdn-cgi/l/email-protection")]')
        )
        # If the node has no sub-tags.
        if not matches:
            matches = list(node.xpath(f'{expression}//text()[contains(., "@")]'))
        if matches:
            for match in matches:
                match = email_re.search(match)
                if match:
                    return match.group(1)
            if error:
                raise Exception(f"No email pattern in {matches}")
            return None
        if error:
            raise Exception(f"No email node in {etree.tostring(node)}")
        return None

    # Helper function for self,get_email
    def _cloudflare_decode(self, link):
        hex_email = link.split("#", 1)[1]
        decoded_email = ""
        key = int(hex_email[:2], 16)

        for i in range(2, len(hex_email) - 1, 2):
            decoded_email += chr(int(hex_email[i : i + 2], 16) ^ key)

        return decoded_email

    def get_phone(self, node, *, area_codes=None, error=True):
        """
        Don't use if multiple telephone numbers are present, e.g. voice and fax.
        If writing a new scraper, check that extensions are captured.
        """
        if area_codes is None:
            area_codes = []
        if isinstance(node, etree._ElementUnicodeResult):
            match = re.search(
                r"(?:\A|\D)(\(?\d{3}\)?\D?\d{3}\D?\d{4}(?:\s*(?:/|x|ext[.:]?|poste)[\s-]?\d+)?)(?:\D|\Z)", node
            )
            if match:
                return match.group(1)
        match = node.xpath('.//a[contains(@href,"tel:")]')
        if match:
            return match[0].attrib["href"].replace("tel:", "")
        if area_codes:
            for area_code in area_codes:
                match = re.search(
                    r"(?:\A|\D)(\(?%d\)?\D?\d{3}\D?\d{4}(?:\s*(?:/|x|ext[.:]?|poste)[\s-]?\d+)?)(?:\D|\Z)" % area_code,  # noqa: UP031
                    node.text_content(),
                )
                if match:
                    return match.group(1)
        else:
            match = re.search(
                r"(?:\A|\D)(\(?\d{3}\)?\D?\d{3}\D?\d{4}(?:\s*(?:/|x|ext[.:]?|poste)[\s-]?\d+)?)(?:\D|\Z)",
                node.text_content(),
            )
            if match:
                return match.group(1)
        if error:
            raise Exception(f"No phone pattern in {node.text_content()}")
        return None

    def get_link(self, node, substring, *, error=True):
        match = node.xpath(f'.//a[contains(@href,"{substring}")]/@href')
        if match:
            return match[0]
        if error:
            raise Exception(f"No link matching {substring}")
        return None

    def get(self, *args, **kwargs):
        return super().get(*args, verify=kwargs.pop("verify", SSL_VERIFY), **kwargs)

    def post(self, *args, **kwargs):
        return super().post(*args, verify=kwargs.pop("verify", SSL_VERIFY), **kwargs)

    def cloudscrape(self, url, verify=SSL_VERIFY):
        response = SCRAPER.get(url, verify=verify)
        response.raise_for_status()
        page = lxml.html.fromstring(response.content)
        page.make_links_absolute(url)
        return page

    def lxmlize(
        self, url, encoding=None, *, user_agent=DEFAULT_USER_AGENT, cookies=None, xml=False, verify=SSL_VERIFY
    ):
        # Sets User-Agent header.
        # https://github.com/jamesturk/scrapelib/blob/5ce0916/scrapelib/__init__.py#L505
        self.user_agent = user_agent

        response = self.get(url, cookies=cookies, verify=verify)
        if encoding:
            response.encoding = encoding

        try:
            text = response.text
            if xml:
                text = text.replace('<?xml version="1.0" encoding="utf-8"?>', "")  # special case: ca_bc
                page = etree.fromstring(text)
            else:
                page = lxml.html.fromstring(text)
        except etree.ParserError as e:
            raise etree.ParserError(f"Document is empty {url}") from e

        meta = page.xpath('//meta[@http-equiv="refresh"]')
        if meta:
            _, url = meta[0].attrib["content"].split("=", 1)
            return self.lxmlize(url, encoding)
        if xml:
            return page
        page.make_links_absolute(url)
        return page

    def csv_reader(self, url, *, delimiter=",", header=False, encoding=None, skip_rows=0, data=None, **kwargs):
        if not data:
            result = urlparse(url)
            if result.scheme == "ftp":
                data = StringIO()
                ftp = FTP(result.hostname)  # noqa: S321
                ftp.login(result.username, result.password)
                ftp.retrbinary(f"RETR {result.path}", lambda block: data.write(block.decode("utf-8")))
                ftp.quit()
                data.seek(0)
            else:
                response = self.get(url, **kwargs)
                if encoding:
                    response.encoding = encoding
                data = StringIO(response.text.strip().removeprefix("\ufeff"))  # BOM
        if skip_rows:
            for _ in range(skip_rows):
                data.readline()
        if header:
            return csv.DictReader(data, delimiter=delimiter)
        return csv.reader(data, delimiter=delimiter)


class CSVScraper(CanadianScraper):
    # File flags
    """Set the CSV file's delimiter."""

    delimiter = ","
    """
    Set the CSV file's encoding, like 'windows-1252' ('utf-8' by default).
    """
    encoding = None
    """
    If `csv_url` is a ZIP file, set the compressed file to read.
    """
    filename = None
    """
    If `csv_url` is an XLS, XLSX or ZIP file, but has no extension, set the extension (like '.xlsx').
    """
    extension = None

    # Table flags
    """
    If the CSV table starts with non-data rows, set the number of rows to skip.
    """
    skip_rows = 0

    # Row flags
    """
    A dictionary of column names to dictionaries of actual to corrected values.
    """
    corrections = {}
    """
    Set whether the jurisdiction has multiple members per division, in which
    case a seat number is appended to the district.
    """
    many_posts_per_area = False
    """
    If `many_posts_per_area` is set, set the roles without seat numbers.
    """
    unique_roles = ("Mayor", "Deputy Mayor", "Regional Chair")
    """
    A format string to generate the district name. Rarely used.
    """
    district_name_format_string = None
    """
    A dictionary of district names to boundary URLs. Rarely used.
    """
    district_name_to_boundary_url = {}
    """
    A dictionary of column names to alternate column names. Rarely used.
    """
    fallbacks = {}
    """
    A dictionary of people's names to lists of alternate names. Rarely used.
    """
    other_names = {}
    """
    The classification of the organization.
    """
    organization_classification = None

    """
    Set the `locale` of the data, like 'fr'.
    """
    column_headers = {
        "fr": {
            "nom du district": "district name",
            "identifiant du district": "district id",
            "rôle": "primary role",
            "prénom": "first name",
            "nom": "last name",
            "genre": "gender",
            "nom du parti": "party name",
            "courriel": "email",
            "url d'une photo": "photo url",
            "url source": "source url",
            "site web": "website",
            "adresse ligne 1": "address line 1",
            "adresse ligne 2": "address line 2",
            "localité": "locality",
            "province": "province",
            "code postal": "postal code",
            "téléphone": "phone",
            "télécopieur": "fax",
            "cellulaire": "cell",
            "facebook": "facebook",
            "twitter": "twitter",
            "date de naissance": "birth date",
        },
    }

    def header_converter(self, s):
        """
        Normalize a column header name.

        By default, lowercase it and replace underscores with spaces (e.g. because Esri fields can't contain spaces).
        """
        header = clean_string(s.lower().replace("_", " "))
        if hasattr(self, "locale"):
            return self.column_headers[self.locale].get(header, header)
        return header

    def is_valid_row(self, row):
        """
        Return whether the row should be imported.

        By default, skip empty rows and rows in which a name component is "Vacant".
        """
        empty = ("", "Vacant")
        if not any(row.values()):
            return False
        if "first name" in row and "last name" in row and ("name" not in row or row["name"] in empty):
            return row["last name"] not in empty and row["first name"] not in empty
        return row["name"] not in empty

    def scrape(self):
        seat_numbers = defaultdict(lambda: defaultdict(int))

        extension = self.extension if self.extension else os.path.splitext(self.csv_url)[1]
        if extension in (".xls", ".xlsx"):
            data = StringIO()
            binary = BytesIO(self.get(self.csv_url).content)
            if extension == ".xls":
                table = agate.Table.from_xls(binary)
            elif extension == ".xlsx":
                table = agate.Table.from_xlsx(binary)
            table.to_csv(data)
            data.seek(0)
        elif extension == ".zip":
            basename = os.path.basename(self.csv_url)
            if not self.encoding:
                self.encoding = "utf-8"
            try:
                response = requests.get(self.csv_url, stream=True)
                with open(basename, "wb") as f:
                    for chunk in response.iter_content():
                        f.write(chunk)
                with ZipFile(basename).open(self.filename, "r") as fp:
                    data = StringIO(fp.read().decode(self.encoding))
            finally:
                os.unlink(basename)
        else:
            data = None

        reader = self.csv_reader(
            self.csv_url,
            delimiter=self.delimiter,
            header=True,
            encoding=self.encoding,
            skip_rows=self.skip_rows,
            data=data,
        )
        reader.fieldnames = [self.header_converter(field) for field in reader.fieldnames]
        for row in reader:
            # ca_qc_laval: "maire et president du comite executif", "conseiller et membre du comite executif"
            # ca_qc_montreal: "Conseiller de la ville; Membre…", "Maire d'arrondissement\nMembre…"
            if row.get("primary role"):
                row["primary role"] = re.split(r"(?: (?:et)\b|[;\n])", row["primary role"], maxsplit=1)[0].strip()

            if not self.is_valid_row(row):
                continue

            for key, corrections in self.corrections.items():
                if not isinstance(corrections, dict):
                    row[key] = corrections(row[key])
                elif row[key] in corrections:
                    row[key] = corrections[row[key]]

            # ca_qc_montreal
            if row.get("last name") and not re.search(r"[a-z]", row["last name"]):
                row["last name"] = re.sub(r"(?<=\b[A-Z])[A-ZÀÈÉ]+\b", lambda x: x.group(0).lower(), row["last name"])

            if row.get("first name") and row.get("last name"):
                name = "{} {}".format(row["first name"], row["last name"])
            else:
                name = row["name"]

            province = row.get("province")
            role = row["primary role"]

            # ca_qc_laval: "maire …", "conseiller …"
            if role not in ("candidate", "member") and not re.search(r"[A-Z]", role):
                role = role.capitalize()

            if self.district_name_format_string:
                if row["district id"]:
                    district = self.district_name_format_string.format(**row)
                else:
                    district = self.jurisdiction.division_name
            elif row.get("district name"):
                district = row["district name"]
            elif self.fallbacks.get("district name"):
                district = row[self.fallbacks["district name"]] or self.jurisdiction.division_name
            else:
                district = self.jurisdiction.division_name

            district = district.replace("–", "—")  # n-dash, m-dash

            # ca_qc_montreal
            if district == "Ville-Marie" and role == "Maire de la Ville de Montréal":
                district = self.jurisdiction.division_name

            if self.many_posts_per_area and role not in self.unique_roles:
                seat_numbers[role][district] += 1
                district = f"{district} (seat {seat_numbers[role][district]})"

            lines = []
            if row.get("address line 1"):
                lines.append(row["address line 1"])
            if row.get("address line 2"):
                lines.append(row["address line 2"])
            if row.get("locality"):
                parts = [row["locality"]]
                if province:
                    parts.append(province)
                if row.get("postal code"):
                    parts.extend(["", row["postal code"]])
                lines.append(" ".join(parts))

            organization_classification = self.organization_classification or self.jurisdiction.classification
            p = CanadianPerson(
                primary_org=organization_classification,
                name=name,
                district=district,
                role=role,
                party=row.get("party name"),
            )
            p.add_source(self.csv_url)

            # ca_on_toronto_candidates:
            #   District name,District ID,…
            #   Toronto Centre,,…
            #   ,3520005,…
            if not row.get("district name") and row.get("district id") and len(row["district id"]) == 7:
                p._related[0].extras["boundary_url"] = "/boundaries/census-subdivisions/{}/".format(row["district id"])

            if row.get("district name") in self.district_name_to_boundary_url:
                p._related[0].extras["boundary_url"] = self.district_name_to_boundary_url[row["district name"]]

            if row.get("gender"):
                p.gender = row["gender"]
            if row.get("photo url"):
                p.image = row["photo url"]

            if row.get("source url"):
                p.add_source(row["source url"])

            if row.get("website"):
                p.add_link(row["website"], note="web site")
            if row.get("facebook"):
                p.add_link(re.sub(r"[#?].+", "", row["facebook"]))
            if row.get("twitter"):
                p.add_link(row["twitter"])

            if row["email"]:
                p.add_contact("email", row["email"].strip().split("\n")[-1])  # ca_qc_montreal
            if lines:
                p.add_contact("address", "\n".join(lines), "legislature")
            if row.get("phone"):
                p.add_contact("voice", row["phone"].split(";", 1)[0], "legislature")  # ca_qc_montreal, ca_on_huron
            if row.get("fax"):
                p.add_contact("fax", row["fax"], "legislature")
            if row.get("cell"):
                p.add_contact("cell", row["cell"], "legislature")
            if row.get("birth date"):
                p.birth_date = row["birth date"]

            if row.get("incumbent"):
                p.extras["incumbent"] = row["incumbent"]

            if name in self.other_names:
                for other_name in self.other_names[name]:
                    p.add_name(other_name)

            yield p


class CanadianJurisdiction(Jurisdiction):
    """Whether to create posts whose labels match division names or type IDs."""

    use_type_id = False
    """
    Which division types to skip when creating posts.
    """
    exclude_types = []
    """
    Whether to skip divisions whose `validFrom` dates are null.
    """
    skip_null_valid_from = False
    """
    The `validFrom` date of the divisions to create (used for candidates).
    """
    valid_from = None
    """
    Override the style of address of members (used for candidates).
    """
    member_role = None

    def __init__(self):
        super().__init__()
        for module, name in (
            ("bills", "Bill"),
            ("bills-incremental", "IncrementalBill"),
            ("committees", "Committee"),
            ("events-incremental", "IncrementalEvent"),
            ("people", "Person"),
            ("votes", "Vote"),
        ):
            try:
                class_name = self.__class__.__name__ + name + "Scraper"
                self.scrapers[module] = getattr(
                    __import__(self.__module__ + "." + module, fromlist=[class_name]), class_name
                )
            except ImportError:
                pass

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)

        leader_role = styles_of_address[self.division_id]["Leader"]
        member_role = self.member_role or styles_of_address[self.division_id]["Member"]

        parent = Division.get(self.division_id)
        # Don't yield posts for premiers.
        if parent._type not in ("province", "territory"):
            # Yield posts to allow ca_on_toronto to make changes.
            post = Post(role=leader_role, label=parent.name, division_id=parent.id, organization_id=organization._id)
            yield post

        children = [
            child
            for child in parent.children()
            if child._type not in ("fed", "place") and child._type not in self.exclude_types
        ]

        for child in children:
            valid_from = child.attrs.get("validFrom")
            valid_through = getattr(child, "valid_through", None)

            # Skip divisions whose `validFrom` dates are null.
            if self.skip_null_valid_from and not valid_from:
                continue

            # Skip divisions that become valid in the future, or that don't match the election date.
            if valid_from and valid_from > datetime.now().strftime("%Y-%m-%d") and valid_from != self.valid_from:
                continue

            # Skip divisions that became invalid in the past.
            if valid_through and valid_through < datetime.now().strftime("%Y-%m-%d"):
                continue

            label = child.id.rsplit("/", 1)[1].capitalize().replace(":", " ") if self.use_type_id else child.name
            # Yield posts to allow ca_on_toronto to make changes.
            post = Post(role=member_role, label=label, division_id=child.id, organization_id=organization._id)
            yield post

        if not children and parent.attrs["posts_count"]:
            for i in range(1, int(parent.attrs["posts_count"])):  # exclude Mayor
                organization.add_post(role=member_role, label=f"{parent.name} (seat {i})", division_id=parent.id)

        yield organization


class CanadianPerson(Person):
    def __init__(self, *, name, district, role, **kwargs):
        """Clean a person's name, district, role and any other attributes."""
        name = clean_name(name)
        district = clean_string(district).replace("&", "and")
        role = clean_string(role)
        if role == "City Councillor":
            role = "Councillor"
        for k, v in kwargs.items():
            if isinstance(v, str):
                kwargs[k] = clean_string(v)
        if not district:
            raise Exception("No district")
        super().__init__(name=name, district=district, role=role, **kwargs)

    def __setattr__(self, name, value):
        """Correct gender values."""
        if name == "gender":
            value = value.lower()
            if value == "m":
                value = "male"
            elif value == "f":
                value = "female"
        super().__setattr__(name, value)

    def add_link(self, url, *, note=""):
        """Correct links without schemes or domains."""
        url = url.strip()
        if url.startswith("www."):
            url = f"http://{url}"
        if re.match(r"\A@[A-Za-z]+\Z", url):
            url = f"https://twitter.com/{url[1:]}"
        self.links.append({"note": note, "url": url})

    def add_contact(self, type, value, note="", area_code=None):
        """Clean and add a contact detail to the person's membership."""
        if type:
            type = clean_string(type)
        if note:
            note = clean_string(note)
        if type in CONTACT_DETAIL_TYPE_MAP:
            type = CONTACT_DETAIL_TYPE_MAP[type]
        if note in CONTACT_DETAIL_NOTE_MAP:
            note = CONTACT_DETAIL_NOTE_MAP[note]

        type = type.lower()

        if type in ("text", "voice", "fax", "cell", "video", "pager"):
            value = self.clean_telephone_number(clean_string(value), area_code=area_code)
        elif type == "address":
            value = self.clean_address(value)
        else:
            value = clean_string(value)

        # The post membership is added before the party membership.
        self._related[0].add_contact_detail(type=type, value=value, note=note)

    def clean_telephone_number(self, s, area_code=None):
        """@see http://www.btb.termiumplus.gc.ca/tpv2guides/guides/favart/index-eng.html?lang=eng&lettr=indx_titls&page=9N6fM9QmOwCE.html."""
        splits = re.split(r"(?:\b \(|/|x|ext[.:]?|p\.|poste)[\s-]?(?=\b|\d)", s, flags=re.IGNORECASE)
        digits = re.sub(r"\D", "", splits[0])

        if len(digits) == 7 and area_code:
            digits = "1" + str(area_code) + digits
        elif len(digits) == 10:
            digits = "1" + digits

        if len(digits) == 11 and digits[0] == "1" and len(splits) <= 2:
            digits = re.sub(r"\A(\d)(\d{3})(\d{3})(\d{4})\Z", r"\1 \2 \3-\4", digits)
            if len(splits) == 2:
                return "{} x{}".format(digits, splits[1].rstrip(")"))
            return digits
        return s

    def clean_address(self, s):
        """Correct the postal code, abbreviate the province or territory name, and format the last line of the address."""
        # The letter "O" instead of the numeral "0" is a common mistake.
        s = re.sub(
            r"\b[A-Z][O0-9][A-Z]\s?[O0-9][A-Z][O0-9]\b", lambda x: x.group(0).replace("O", "0"), clean_string(s)
        )
        for k, v in province_or_territory_abbreviations().items():
            # Replace a province/territory name with its abbreviation.
            s = re.sub(
                r"[,\n ]+"
                r"\(?" + k + r"\)?"
                r"(?=(?:[,\n ]+Canada)?(?:[,\n ]+[A-Z][0-9][A-Z]\s?[0-9][A-Z][0-9])?\Z)",
                " " + v,
                s,
            )
        # Add spaces between province/territory abbreviation, FSA and LDU and remove "Canada".
        return re.sub(
            r"[,\n ]+" r"([A-Z]{2})" r"(?:[,\n ]+Canada)?" r"[,\n ]+([A-Z][0-9][A-Z])\s?([0-9][A-Z][0-9])" r"\Z",
            r" \1  \2 \3",
            s,
        )


whitespace_re = re.compile(r"\s+", flags=re.UNICODE)
whitespace_and_newline_re = re.compile(r"[^\S\n]+", flags=re.UNICODE)
honorific_prefix_re = re.compile(r"\A(?:Councillor|Dr|Hon|M|Mayor|Mme|Mr|Mrs|Ms|Miss)\.? ")
honorific_suffix_re = re.compile(r", (?:Ph\.D, Q\.C\.)\Z")
province_or_territory_abbreviation_memo = {}

table = {
    ord("\u200b"): " ",  # zero-width space
    ord("’"): "'",
    ord("\xc2"): "\xa0",  # non-breaking space if mixing ISO-8869-1 into UTF-8
}


def province_or_territory_abbreviations():
    if not province_or_territory_abbreviation_memo:
        province_or_territory_abbreviation_memo["PEI"] = "PE"
        for division in Division.all("ca"):
            if division._type in ("province", "territory"):
                abbreviation = division.id.rsplit(":", 1)[1].upper()
                province_or_territory_abbreviation_memo[division.name] = abbreviation
                province_or_territory_abbreviation_memo[division.attrs["name_fr"]] = abbreviation
    return province_or_territory_abbreviation_memo


def clean_string(s):
    return re.sub(r" *\n *", "\n", whitespace_and_newline_re.sub(" ", str(s).translate(table)).strip())


def clean_name(s):
    name = honorific_suffix_re.sub("", whitespace_re.sub(" ", str(s).translate(table)).strip())
    if name.count(" ") > 1:
        return honorific_prefix_re.sub("", name)  # Avoid truncating names like "Hon Chan"
    return name


def clean_type_id(type_id):
    # "Uppercase characters should be converted to lowercase."
    type_id = type_id.lower()
    # "Spaces should be converted to underscores."
    type_id = re.sub(r" ", "_", type_id)
    # "All invalid characters should be converted to tilde (~)."
    return re.sub(r"[^\w.~-]", "~", type_id, flags=re.UNICODE)


def clean_french_prepositions(s):
    return re.sub(r"\b(?:d'|de (?:l'|la )?|du |des |l')", "", clean_string(s), flags=re.IGNORECASE)
