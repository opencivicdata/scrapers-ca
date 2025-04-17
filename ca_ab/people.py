import csv
from io import StringIO
from itertools import zip_longest

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.assembly.ab.ca/txt/mla_home/contacts.csv"
MEMBER_INDEX_URL = "https://www.assembly.ab.ca/members/members-of-the-legislative-assembly"

PARTIES = {
    "AL": "Alberta Liberal Party",
    "AP": "Alberta Party",
    "IC": "Independent Conservative",
    "IND": "Independent",
    "FCP": "Freedom Conservative Party",
    "ND": "Alberta New Democratic Party",
    "NDP": "Alberta New Democratic Party",
    "PC": "Progressive Conservative Association of Alberta",
    "UC": "United Conservative Party",
    "UCP": "United Conservative Party",
    "W": "Wildrose Alliance Party",
}


def get_party(abbr):
    """Return full party name from abbreviation."""
    return PARTIES[abbr]


OFFICE_FIELDS = (
    "Address Type",
    "Address Line1",
    "Address Line2",
    "City",
    "Province",
    "Country",
    "Postal Code",
    "Phone Number",
    "Fax Number",
)

ADDRESS_FIELDS = (
    "Address Line1",
    "Address Line2",
    "City",
    "Province",
    "Country",
)


class AlbertaPersonScraper(CanadianScraper):
    def scrape(self):
        index = self.lxmlize(MEMBER_INDEX_URL)
        csv_text = self.get(COUNCIL_PAGE).text.strip()
        csv_text = "\n".join(csv_text.split("\n")[3:])  # discard first 3 rows
        reader = csv.reader(StringIO(csv_text))
        # make unique field names for the two sets of address fields
        field_names = next(reader)
        for name in OFFICE_FIELDS:
            assert field_names.count(name) == 2
            field_names[field_names.index(name)] = f"{name} 1"
            field_names[field_names.index(name)] = f"{name} 2"
        rows = [dict(zip_longest(field_names, row)) for row in reader]
        assert rows, "No members found"
        for mla in rows:
            name = "{} {} {}".format(
                mla["MLA First Name"],
                mla["MLA Middle Names"],
                mla["MLA Last Name"],
            )
            if name.strip() == "":
                continue
            party = get_party(mla["Caucus"])
            name_without_status = name.split(",")[0]
            row_xpath = '//td[normalize-space()="{}"]/..'.format(
                mla["Constituency Name"],
            )
            (detail_url,) = index.xpath(f"{row_xpath}//a/@href")
            (photo_url,) = index.xpath(f"{row_xpath}//img/@src")
            district = mla["Constituency Name"]
            if district == "Calgary-Bhullar-McCall":
                district = "Calgary-McCall"
            p = Person(
                primary_org="legislature",
                name=name_without_status,
                district=district,
                role="MLA",
                party=party,
                image=photo_url,
            )
            p.add_source(COUNCIL_PAGE)
            p.add_source(detail_url)
            if mla["Email"]:
                p.add_contact("email", mla["Email"])
            elif mla.get("MLA Email"):
                p.add_contact("email", mla["MLA Email"])

            addresses = [(1, "legislature"), (2, "constituency")]
            if not mla["Address Type 1"].strip():
                addresses.pop(0)
            else:
                assert mla["Address Type 1"] == "Legislature Office"
            if not mla["Address Type 2"]:
                addresses.pop()
            else:
                assert mla["Address Type 2"] == "Constituency Office"

            for suffix, note in addresses:
                for key, contact_type in (("Phone", "voice"), ("Fax", "fax")):
                    value = mla[f"{key} Number {suffix}"]
                    if value and value != "Pending":
                        p.add_contact(contact_type, value, note)
                address = ", ".join(filter(bool, [mla[f"{field} {suffix}"] for field in ADDRESS_FIELDS]))
                if address:
                    p.add_contact("address", address, note)

            members_page = self.lxmlize(detail_url)

            roles = members_page.xpath('//div[contains(@class, "heading-block")]/following-sibling::h4/div/text()')
            if roles:
                p.extras["roles"] = roles

            yield p
