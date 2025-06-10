# https://github.com/opencivicdata/scrapers-ca/blob/b19f84783efe046fac96426ebe6e1d7c8dcf1fcd/ca_candidates/people.py
import csv
import json
import logging
import re
from io import StringIO
from urllib.parse import urlsplit

import lxml.etree
import requests
import scrapelib
from opencivicdata.divisions import Division
from pupa.utils import get_pseudo_id
from unidecode import unidecode

from utils import CUSTOM_USER_AGENT, CanadianScraper
from utils import CanadianPerson as Person

SOCIAL_MEDIA_DOMAINS = (
    "facebook.com",
    "instagram.com",
    "linkedin.com",
    "twitter.com",
    "x.com",
    "youtube.com",
)
CLEAN_EMAIL_REGEX = re.compile(r"mailto:|\?subject=.+")

TRANSLATION_TABLE = str.maketrans("\u2013\u2014-", "   ", r"\u200f")  # n-dash, m-dash, right-to-left mark
CONSECUTIVE_WHITESPACE_REGEX = re.compile(r"\s+")
CORRECTIONS = {
    # Different names.
    "Kelowna Lake Country": "Kelowna",
    "Nonafot Nunavut": "Nunavut",
    # Typographic errors.
    "Northwest Territores": "Northwest Territories",
}

logger = logging.getLogger(__name__)


class CanadaCandidatesPersonScraper(CanadianScraper):
    normalized_names = {}
    boundary_ids = {}
    elections_canada_candidates = {}
    division_map = {}

    def normalize_district(self, district):
        # Ignore accents, hyphens, lettercase, and leading, trailing and consecutive whitespace.
        district = unidecode(district.translate(TRANSLATION_TABLE)).title().strip()
        district = CONSECUTIVE_WHITESPACE_REGEX.sub(" ", district)
        return CORRECTIONS.get(district, district)

    def normalized_candidate_names(self, candidate_name):
        candidate_name = unidecode(candidate_name.translate(TRANSLATION_TABLE)).title().strip()
        return CONSECUTIVE_WHITESPACE_REGEX.sub(" ", candidate_name)

    def get_district(self, district):
        try:
            return self.normalized_names[self.normalize_district(district)]
        except KeyError:
            logger.exception("")

    def scrape(self):
        # Create list mapping names to IDs.
        for division in Division.get("ocd-division/country:ca").children("ed"):
            if "2023" in division.id:
                self.normalized_names[self.normalize_district(division.name)] = division.name
                self.normalized_names[self.normalize_district(division.attrs["name_fr"])] = division.name
                self.boundary_ids[division.name] = re.search(r"(\d+)-2023\Z", division.id).group(1)
                self.division_map[re.search(r"(\d+)-2023\Z", division.id).group(1)] = self.normalize_district(
                    division.name
                )

        representatives = json.loads(
            self.get("http://represent.opennorth.ca/representatives/house-of-commons/?limit=0").text
        )["objects"]
        self.incumbents = [representative["name"] for representative in representatives]

        crowdsourcing = {}
        url = "https://docs.google.com/spreadsheets/d/1g0yaE3dr8N7pF2K9TSp2VApJHmHDyGMqH6-Ba5SQLts/export?format=csv&id=1g0yaE3dr8N7pF2K9TSp2VApJHmHDyGMqH6-Ba5SQLts"

        response = requests.get(url)
        response.encoding = "utf-8"

        key = ""
        seen = {}
        scraped_parties = (
            "Bloc Québécois",
            "Christian Heritage",
            "Communist",
            "Conservative",
            "Forces et Démocratie",
            "Green Party",
            "Independent",
            "Liberal",
            "Libertarian",
            "Marxist–Leninist",
            "NDP",
        )

        for row in csv.DictReader(StringIO(response.text)):
            if "District Number" in row:
                boundary_id = row["District Number"]
                if not re.search(r"\A\d{5}\Z", boundary_id):
                    boundary_id = self.boundary_ids[boundary_id]
                key = "{}/{}/{}".format(row["Party name"], boundary_id, row["Name"])

                if crowdsourcing.get(key):
                    self.warning(f"{key} already exists")
                else:
                    if row["Gender"] == "M":
                        gender = "male"
                    elif row["Gender"] == "F":
                        gender = "female"
                    else:
                        gender = None

                    crowdsourcing[key] = {
                        "gender": gender,
                        "email": row["Email"],
                        "image": row["Photo URL"],
                        "facebook": row["Facebook"],
                        "instagram": row["Instagram"],
                        "twitter": row["Twitter"],
                        "linkedin": row["LinkedIn"],
                        "youtube": row["YouTube"],
                    }

            steps = {
                "gender": (
                    lambda p: p.gender,
                    lambda p, value: setattr(p, "gender", value),
                ),
                "email": (
                    lambda p: next(
                        (
                            contact_detail["value"]
                            for contact_detail in p._related[0].contact_details
                            if contact_detail["type"] == "email"
                        ),
                        None,
                    ),
                    lambda p, value: p.add_contact("email", value),
                ),
                "image": (
                    lambda p: p.image,
                    lambda p, value: setattr(p, "image", value),
                ),
            }

        self.scrape_elections_canada()

        for party in (
            "liberal",
            "ndp",
            "green",
            "conservative",
            "missing_elections_canada",
        ):
            try:
                for p in getattr(self, f"scrape_{party}")():
                    if not p._related[0].post_id:
                        raise Exception(f"No post_id for {p.name} of {p._related[1].organization_id}")

                    # Uniquely identify the candidate.
                    boundary_id = get_pseudo_id(p._related[0].post_id)["label"]
                    partyname = get_pseudo_id(p._related[1].organization_id)["name"]
                    if not re.search(r"\A\d{5}\Z", boundary_id):
                        try:
                            boundary_id = self.boundary_ids[boundary_id]
                        except KeyError:
                            raise Exception(f"KeyError: '{boundary_id.lower()}' on {party}") from None

                    key = f"{partyname}/{boundary_id}"
                    try:
                        elections_canada_candidate = self.elections_canada_candidates[key]
                        phone_to_be_added = True
                        if elections_canada_candidate["phone"] == "":
                            phone_to_be_added = False
                        for contact_detail in p._related[0].contact_details:
                            if (
                                phone_to_be_added
                                and contact_detail["type"] == "voice"
                                and contact_detail["value"]
                                == p.clean_telephone_number(elections_canada_candidate["phone"])
                            ):
                                phone_to_be_added = False
                        if phone_to_be_added:
                            p.add_contact("voice", elections_canada_candidate["phone"], "Work")
                        self.elections_canada_candidates[key]["processed"] = True
                    except KeyError:
                        self.warning(f"Candidate not present in elections canada scrpe {key}")
                        continue

                    # Names from Elections Canada may differ, but there may also be
                    # multiple independents per district.
                    seen_key = key if partyname == "Independent" else f"{partyname}/{boundary_id}"
                    if seen.get(seen_key):
                        # We got the candidate from a scraper.
                        if party == "elections_canada":
                            continue
                        # We got the same candidate from different scrapers.
                        else:
                            raise Exception(f"{seen_key} seen in {seen[seen_key]} during {party}")
                    elif party == "elections_canada":
                        # We should have gotten the candidate from a scraper.
                        if partyname in scraped_parties:
                            if partyname == "Independent":
                                self.error(f"{seen_key} not seen")
                            else:
                                self.warning(f"{seen_key} not seen")
                        # We are getting the candidate from a scraper.
                        else:
                            seen[seen_key] = party

                    # Merge the crowdsourced data.
                    if crowdsourcing.get(key):
                        o = crowdsourcing[key]

                        links = {}
                        for link in p.links:
                            domain = ".".join(urlsplit(link["url"]).netloc.split(".")[-2:])
                            if domain in ("facebook.com", "fb.com"):
                                links["facebook"] = link["url"]
                            elif domain == "instagram.com":
                                links["instagram"] = link["url"]
                            elif domain == "linkedin.com":
                                links["linkedin"] = link["url"]
                            elif domain == "twitter.com":
                                links["twitter"] = link["url"]
                            elif domain == "youtube.com":
                                links["youtube"] = link["url"]

                        for prop, (getter, setter) in steps.items():
                            if o[prop]:
                                if prop == "email" and ".gc.ca" in o[prop]:
                                    self.info(f"{key}: skipping email = {o[prop]}")
                                else:
                                    scraped = getter(p)
                                    if not scraped:
                                        setter(p, o[prop])
                                        self.debug(f"{key}: adding {prop} = {o[prop]}")
                                    elif scraped.lower() != o[prop].lower() and prop != "image":
                                        self.warning(f"{key}: expected {prop} to be {scraped}, not {o[prop]}")

                        for prop in ["facebook", "instagram", "linkedin", "twitter", "youtube"]:
                            if o[prop]:
                                scraped = links.get(prop)
                                entered = re.sub(
                                    r"/timeline/\Z|\?(f?ref|lang|notif_t)=.+|\?_rdr\Z",
                                    "",
                                    o[prop].replace("@", "").replace("http://twitter.com/", "https://twitter.com/"),
                                )  # Facebook, Twitter
                                if not scraped:
                                    p.add_link(entered)
                                    self.debug(f"{key}: adding {prop} = {entered}")
                                elif scraped.lower() != entered.lower():
                                    self.warning(f"{key}: expected {prop} to be {scraped}, not {entered}")
                    yield p

            except IndexError:
                logger.exception("")

    def scrape_ndp(self):
        delete_regex = re.compile("[ '.-]")

        start_url = "https://www.ndp.ca/candidates"
        page = self.lxmlize(start_url)

        candidates = page.xpath('//div[@class="campaign-civics-list-items"]/div')
        assert len(candidates), "No NDP candidates found"

        for candidate in candidates:
            district = self.get_district(candidate.xpath("./div/div/div")[1].text_content())
            if district is None:
                continue

            name = candidate.xpath("./div/div/div")[0].text_content()
            image = f"https://www.ndp.ca{candidate.xpath('./div/img')[0].get('data-img-src')}"

            p = Person(
                primary_org="lower",
                name=name,
                district=district,
                role="candidate",
                party="New Democratic Party",
                image=image,
            )

            subdomain = delete_regex.sub("", unidecode(name).lower())
            if subdomain == "arlingtonantoniosantiago":
                subdomain = "arlingtonsantiago"

            if subdomain == "tammybentz":
                url = f"https://{subdomain}.ndp.ca/contact"
            elif subdomain in {
                "huguesboilymaltais",
                "juliegirardlemay",
                "lisegaron",
                "tommybureau",
            }:
                url = f"https://{subdomain}.npd.ca"
            else:
                url = f"https://{subdomain}.ndp.ca"

            p.add_source(start_url)
            p.add_source(url)

            try:
                candidatepage = self.lxmlize(url)

                if email := candidatepage.xpath('//a[contains(@href, "mailto:")]/@href'):
                    p.add_contact("email", CLEAN_EMAIL_REGEX.sub("", email[0]))

                for xpath in (
                    "//a[contains(@href, 'facebook') or contains(@href, 'fb')]/@href",
                    "//a[contains(@href, 'instagram')]/@href",
                    "//a[contains(@href, 'twitter')]/@href",
                    "//a[contains(@href, 'youtube')]/@href",
                ):
                    if element := candidatepage.xpath(xpath):
                        p.add_link(element[0])

                if phone := candidatepage.xpath('//a[contains(@href, "tel:")]/@href'):
                    p.add_contact("voice", phone[0].replace("tel:", ""), "office")
            except (lxml.etree.ParserError, requests.RequestException):
                # requests.exceptions.SSLError: HTTPSConnectionPool(host='nimamachouf.org', port=443)
                # lxml.etree.ParserError: Document is empty https://avilewis.ndp.ca
                logger.exception("")

            yield p

    def scrape_liberal(self):
        start_url = "https://liberal.ca/your-liberal-candidates/"
        page = self.lxmlize(start_url, user_agent=CUSTOM_USER_AGENT)

        candidates = page.xpath('//div[@class="person-listing-container"]/article')
        assert len(candidates), "No Liberal candidates found"

        for candidate in candidates:
            district = self.get_district(candidate.xpath(".//h3[contains(@class, 'person__riding-name')]/text()")[0])
            if district is None:
                continue

            name = candidate.xpath(".//h2[contains(@class, 'person__name')]/text()")[0]
            # Liberal party has got the wrong name here as of 27.3.25
            if name == "Ron Thiering" and district == "Edmonton Strathcona":
                continue

            p = Person(primary_org="lower", name=name, district=district, role="candidate", party="Liberal Party")
            # image is still a div element -> extract url

            p.add_source(start_url)

            for link in candidate.xpath(".//div[contains(@class, 'person__link-row-container')]")[0].xpath(
                "./div/a/@href"
            ):
                if any(domain in link for domain in SOCIAL_MEDIA_DOMAINS):
                    p.add_link(link)
                else:
                    try:
                        candidatepage = self.lxmlize(link, user_agent=CUSTOM_USER_AGENT)
                        if email := candidatepage.xpath('//a[contains(@href, "mailto:")]/@href'):
                            p.add_contact("email", CLEAN_EMAIL_REGEX.sub("", email[0]).replace("Canada￼", ""))

                        p.add_source(link)
                    except (
                        lxml.etree.ParserError,
                        requests.RequestException,
                        requests.exceptions.ConnectionError,
                        scrapelib.HTTPError,
                    ) as e:
                        logger.warning("%s (%s)", e, link)

            yield p

    def scrape_green(self):
        start_url = "https://www.greenparty.ca/en/candidates/"

        candidates = []
        for page_number in range(1, 343 // 20 + 1):  # 343 divisions, 20 candidates per page
            url = f"{start_url}page/{page_number}"
            try:
                page = self.lxmlize(url)
            except scrapelib.HTTPError as e:
                logger.warning("%s (%s)", e, url)
            else:
                candidates += page.xpath('.//div[@class="grid-4 gpc-candidates-grid"]/article')

        assert len(candidates), "No Green candidates found"

        for candidate in candidates:
            district = self.get_district(candidate.xpath("./div/p/text()")[0])
            if district is None:
                continue

            name = "".join(candidate.xpath("./div/h2/a/text()"))
            name = self.normalized_candidate_names(name)
            image = candidate.xpath("./a/img/@src")[0]

            p = Person(
                primary_org="lower", name=name, district=district, role="candidate", party="Green Party", image=image
            )

            url = candidate.xpath("./a/@href")[0]
            p.add_source(start_url)
            p.add_source(url)

            candidatepage = self.lxmlize(url)

            if email := candidatepage.xpath('//a[contains(@href, "mailto:")]/@href'):
                p.add_contact("email", CLEAN_EMAIL_REGEX.sub("", email[0]))

            for link in candidatepage.xpath(
                '//ul[@class="wp-block-social-links gpc-candidate-socials is-layout-flex wp-block-social-links-is-layout-flex"]/li/a/@href'
            ):
                if any(domain in link for domain in SOCIAL_MEDIA_DOMAINS):
                    p.add_link(link)

            yield p

    def scrape_conservative(self):
        start_url = "https://www.conservative.ca/candidates"
        page = self.lxmlize(start_url)

        candidates = page.xpath('//div[@class="candidate-grid"]/div')
        assert len(candidates)

        for candidate in candidates:
            name = CONSECUTIVE_WHITESPACE_REGEX.sub(" ", " ".join(candidate.xpath("./div/div/h3/text()")))
            district = self.get_district(candidate.xpath("./div/div/p")[0].text_content())
            if district is None:
                continue

            p = Person(primary_org="lower", name=name, district=district, role="candidate", party="Conservative Party")

            p.add_source(start_url)

            url = candidate.xpath("./div/a/@href")
            if url and url[0] != start_url:
                url = url[0]
                p.add_source(url)

                try:
                    candidatepage = self.lxmlize(url)

                    email = self.get_email(candidatepage, error=False)
                    if email:
                        p.add_contact("email", email)

                    phone = self.get_phone(candidatepage, error=False)
                    if phone is not None:
                        phone = phone.replace("https://", "").replace("%20", " ")
                    if phone:
                        p.add_contact("voice", phone, "office")

                except (
                    lxml.etree.ParserError,
                    requests.RequestException,
                    requests.exceptions.ConnectionError,
                    scrapelib.HTTPError,
                ):
                    logger.exception("")

            for link in candidate.xpath("./div/ul/li/a/@href"):
                if any(domain in link for domain in SOCIAL_MEDIA_DOMAINS):
                    p.add_link(link)
            yield p

    def scrape_elections_canada(self):
        name = ""
        party = ""

        url_ec = "https://docs.google.com/spreadsheets/d/1vcG7xsvUMtxrYmaswGY4MMbVf_lwJp3yoCOe7U75cQ0/export?format=csv&id=1vcG7xsvUMtxrYmaswGY4MMbVf_lwJp3yoCOe7U75cQ0"
        response_ec = requests.get(url_ec)
        response_ec = response_ec.content.decode("utf-8", errors="replace").replace("\x00", "")

        for row in csv.DictReader(StringIO(response_ec)):
            name = (
                row["Candidate's First Name / Prénom du candidat"]
                + " "
                + row["Candidate's Family Name / Nom de famille du candidat"]
            )
            party = row["Political Affiliation"]
            if "Liberal Party of Canada" in party:
                party = "Liberal Party"
            elif "Conservative Party of Canada" in party:
                party = "Conservative Party"
            elif "Green Party of Canada" in party:
                party = "Green Party"
            elif "No Affiliation" in party:
                party = "Independent"
            boundary_id = row["Electoral District Number / No de circonscription"]

            phone = row[
                "Candidate's Campaign Office Telephone Number / Numéro de téléphone du bureau de campagne du candidat"
            ]
            if not phone:
                phone = ""
            self.elections_canada_candidates[f"{party}/{boundary_id}"] = {
                "phone": phone,
                "processed": False,
                "name": name,
                "district": self.division_map[boundary_id],
                "party": party,
            }

    def scrape_missing_elections_canada(self):
        for key in self.elections_canada_candidates:
            candidate = self.elections_canada_candidates[key]
            if not candidate["processed"]:
                p = Person(
                    primary_org="lower",
                    name=self.normalized_candidate_names(candidate["name"]),
                    district=self.get_district(candidate["district"]),
                    role="candidate",
                    party=candidate["party"],
                )
                p.add_source("https://www.elections.ca/content2.aspx?section=can&dir=cand/lst&document=index&lang=e")
                yield p
