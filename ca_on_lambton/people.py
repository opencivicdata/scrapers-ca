from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = (
    "http://www.lambtononline.ca/home/government/accessingcountycouncil/countycouncillors/Pages/default.aspx"
)


class LambtonPersonScraper(CanadianScraper):
    def scrape(self):
        councillor_seat_number = 1

        page = self.lxmlize(COUNCIL_PAGE)
        councillors = page.xpath('//div[@id="content"]//table//tr[position() mod 2 = 1]')
        assert len(councillors), "No councillors found"
        for councillor in councillors:
            text = councillor.xpath(".//strong/text()")[0]
            if "Deputy Warden" in text:
                role = "Deputy Warden"
                name = text.replace("Deputy Warden", "")
                district = "Lambton"
            elif "Warden" in text:
                role = "Warden"
                name = text.replace("Warden", "")
                district = "Lambton"
            else:
                role = "Councillor"
                name = text
                district = "Lambton (seat {})".format(councillor_seat_number)
                councillor_seat_number += 1

            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)

            p.image = councillor.xpath(".//img/@src")[0]
            p.add_contact("email", self.get_email(councillor))

            yield p
