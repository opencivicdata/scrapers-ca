from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.stjohns.ca/en/city-hall/mayor-and-council.aspx"


class StJohnsPersonScraper(CanadianScraper):
    def scrape(self):
        councillor_seat_number = 1

        page = self.lxmlize(COUNCIL_PAGE)
        councillors = page.xpath('//div[@class="iCreateDynaToken"]/ul//a/@href')
        assert len(councillors), "No councillors found"
        for url in councillors:
            page = self.lxmlize(url)
            role, name = page.xpath("//h1")[0].text_content().strip().split(" ", 1)
            if role == "Deputy":
                role = "Deputy Mayor"
                name = name.split(" ", 1)[1]
            description = page.xpath('//div[@data-lm-tokenid="StandardOneColumnTK1"]/p')[0].text_content()
            if "Ward" in description:
                index = description.find("Ward")
                district = description[index : index + 6]
            else:
                district = "St. John's"
                if role not in ("Mayor", "Deputy Mayor"):
                    role = "Councillor at Large"
                    district = f"St. John's (seat {councillor_seat_number})"
                    councillor_seat_number += 1

            email = self.get_email(page)
            phone = self.get_phone(page)
            photo = page.xpath('//div[@class="fbg-row lb-imageBox cm-datacontainer"]//img/@src')[0]

            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.image = photo
            p.add_contact("voice", phone, "legislature")
            p.add_contact("email", email)
            p.add_source(COUNCIL_PAGE)
            p.add_source(url)

            yield p
