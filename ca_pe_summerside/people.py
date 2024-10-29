import re

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://summerside.hosted.civiclive.com/mayor_and_council"


def decode_email(hex_email):
    decoded_email = ""
    key = int(hex_email[:2], 16)

    for i in range(2, len(hex_email) - 1, 2):
        decoded_email += chr(int(hex_email[i : i + 2], 16) ^ key)

    return decoded_email


class SummersidePersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE, user_agent="Mozilla/5.0")

        councillors = page.xpath('//ul[@class="sidenav"]//a[contains(., "Mayor") or contains(., "Councillor")]/@href')
        assert len(councillors), "No councillors found"
        for url in councillors:
            page = self.lxmlize(url, user_agent="Mozilla/5.0")

            role, name = page.xpath('//div[@id="pagetitle"]')[0].text_content().split(" /")[0].split(" ", 1)

            if role == "Mayor":
                district = "Summerside"
            else:
                district = re.search(
                    r"(?<=Ward\s\d:\s).*(?=\n|\s$|)",
                    page.xpath('//div[contains(@id, "ContentPlaceHolder")]//img/parent::*')[0].text_content(),
                ).group(0)
                district = (
                    district.replace(" -", "-").replace("- ", "-").replace("-", "—").replace("Councillor", "").strip()
                )
            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)
            p.add_source(url)

            photo = page.xpath('//div[contains(@id, "ContentPlaceHolder")]//img/@src')[0]
            phone = self.get_phone(page)
            hex_email = page.xpath('//div[contains(@id, "ContentPlaceHolder")]//@data-cfemail')[0]
            email = decode_email(hex_email)

            p.image = photo
            p.add_contact("voice", phone, "legislature")
            p.add_contact("email", email)

            yield p
