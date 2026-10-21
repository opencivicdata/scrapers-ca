import re

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.thunderbay.ca/en/city-hall/mayor-and-council-profiles.aspx"

AT_LARGE = {
    "Rajni Agarwal",
    "Albert Aiello",
    "Mark Bentz",
    "Shelby Ch'ng",
    "Kasey Etreni",
}
WARDS = {
    "Andrew Foulds": "Current River",
    "Michael Zussino": "Red River",
    "Brian Hamilton": "McKellar",
    "Trevor Giertuga": "McIntyre",
    "Dominic Pasqualino": "Northwood",
    "Kristen Oliver": "Westfort",
    "Greg Johnsen": "Neebing",
}


class ThunderBayPersonScraper(CanadianScraper):
    def clean_name(self, name):
        return " ".join(
            name.replace("\xa0", " ").replace("Ch\xe2\x80\x99ng", "Ch'ng").replace("Ch\u2019ng", "Ch'ng").split()
        )

    def scrape(self):
        # SSLError(SSLError(1, '[SSL: DH_KEY_TOO_SMALL] dh key too small (_ssl.c:1133)'))
        page = self.lxmlize(COUNCIL_PAGE, verify=False)

        councillors = page.xpath('//table[contains(@class, "icrtAccordion")][.//td[@data-name="accParent"]]')
        assert len(councillors), "No councillors found"

        seat_number = 1
        for councillor in councillors:
            name = self.clean_name(
                councillor.xpath('normalize-space(.//td[@data-name="accParent"]//*[self::h5 or self::h6][1])')
            )
            if not name:
                continue

            if name.startswith("Mayor "):
                name = name[len("Mayor ") :]

            if name == "Ken Boshcoff":
                role = "Mayor"
                district = "Thunder Bay"
            elif name in AT_LARGE:
                role = "Councillor at Large"
                district = f"Thunder Bay (seat {seat_number})"
                seat_number += 1
            elif name in WARDS:
                role = "Councillor"
                district = WARDS[name]
            else:
                raise ValueError(f"Unknown Thunder Bay councillor: {name}")

            contact = councillor.xpath('.//td[@data-name="accChild"]')[0]
            email = self.get_email(contact, error=False)
            phone = self.get_phone(contact, area_codes=[807], error=False)

            text = " ".join(contact.text_content().split())
            image_match = re.search(r"(https?://\S+\.(?:jpe?g|png))", text)

            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)
            if email:
                p.add_contact("email", email)
            if phone:
                p.add_contact("voice", phone, "legislature")
            if image_match:
                p.image = image_match.group(1)

            yield p
