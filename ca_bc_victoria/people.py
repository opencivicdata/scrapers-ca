from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.victoria.ca/city-government/mayor-council/members-council"
MAYOR_PAGE = "https://www.victoria.ca/city-government/mayor-council/mayor-marianne-alto"  # will probably break if the mayor changes


class VictoriaPersonScraper(CanadianScraper):
    def scrape(self):
        seat_number = 1
        page = self.lxmlize(COUNCIL_PAGE)

        councillors = page.xpath(
            '//article[@class="node node--type-councillor node--view-mode-list-item list-item flex fd-r fd-c-mq-m g-32"]'
        )

        for councillor in councillors:
            role, name = councillor.xpath(".//h3/a/span")[0].text_content().split(" ", 1)
            photo = councillor.xpath(".//img/@src")[0]
            email = self.get_email(councillor)
            phone = self.get_phone(councillor)
            url = councillor.xpath(".//h3/a/@href")[0]

            district = "Victoria (seat {})".format(seat_number)
            seat_number += 1

            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.image = photo
            p.add_contact("email", email)
            p.add_contact("voice", phone, "legislature")
            p.add_source(COUNCIL_PAGE)
            p.add_source(url)

            yield p

        page = self.lxmlize(MAYOR_PAGE)
        role, name = page.xpath("//h1/span")[0].text_content().split(" ", 1)
        photo = councillor.xpath('//div[@class="field__item"]/img/@src')[0]
        email = self.get_email(page)
        phone = self.get_phone(page)
        p = Person(primary_org="legislature", name=name, district="Victoria", role=role)
        p.image = photo
        p.add_contact("email", email)
        p.add_contact("voice", phone, "legislature")
        p.add_source(MAYOR_PAGE)

        yield p
