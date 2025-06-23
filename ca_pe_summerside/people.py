import re

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.summerside.ca/city_governance/senior_leadership_mayor_council"


def decode_email(hex_email):
    decoded_email = ""
    key = int(hex_email[:2], 16)

    for i in range(2, len(hex_email) - 1, 2):
        decoded_email += chr(int(hex_email[i : i + 2], 16) ^ key)

    return decoded_email


class SummersidePersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE, user_agent="Mozilla/5.0")

        councillors = page.xpath('//div[@class="subpageContent"]//div[@class="ptl_portlet_vertical"]')
        assert len(councillors), "No councillors found"
        for councillor in councillors:
            role_name = councillor.xpath('.//div[@class="LName"]')[0].text_content()
            if "/" in role_name:
                role, name = role_name.split(" / ")[1].split(" ", 1)
            else:
                role, name = role_name.split(" ", 1)

            if role == "Mayor":
                district = "Summerside"
            else:
                district = re.search(
                    r"(?<=Ward\s\d:\s).*",
                    councillor.xpath('.//div[@class="LContact"]/ul/li')[0].text_content(),
                ).group(0)
                district = (
                    district.replace(" -", "-").replace("- ", "-").replace("-", "—").replace("Councillor", "").strip()
                )
            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)

            photo = councillor.xpath(".//img/@src")[0]
            phone = self.get_phone(page)

            hex_email = councillor.xpath(".//@data-cfemail")[0]
            email = decode_email(hex_email)

            p.image = photo
            p.add_contact("voice", phone, "legislature")
            p.add_contact("email", email)

            yield p
