import re

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.coquitlam.ca/Directory.aspx?DID=54"


class CoquitlamPersonScraper(CanadianScraper):
    def scrape(self):
        def build_email(script):
            w = re.findall(r'w = "(.*?)"', script)[0]
            x = re.findall(r'x = "(.*?)"', script)[0]
            return w + "@" + x

        councillor_seat_number = 1

        page = self.lxmlize(COUNCIL_PAGE, user_agent="Mozilla/5.0")
        councillors = page.xpath('//table[contains(@id, "cityDirectoryDepartmentDetails")]/tr')
        assert len(councillors), "No councillors found"
        for councillor in councillors:
            name = " ".join(
                reversed(councillor.xpath(".//a")[0].text_content().strip().split(", "))
            )  # Names formatted as Last, First
            role = councillor.xpath("./td[2]/span")[0].text_content()
            email_script = councillor.xpath(".//td[3]//script")[0].text_content()  # Site uses JS to build the emails
            email = build_email(email_script)
            phone = self.get_phone(councillor)
            url = councillor.xpath(".//a/@href")[0]

            page = self.lxmlize(url)
            image = page.xpath('//img[@class="imageAlignRight"]/@src')

            if role == "Mayor":
                district = "Coquitlam"
            else:
                district = f"Coquitlam (seat {councillor_seat_number})"
                councillor_seat_number += 1

            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)
            p.add_source(url)

            p.image = image[0]
            p.add_contact("email", email)
            p.add_contact("voice", phone, "legislature")

            yield p
