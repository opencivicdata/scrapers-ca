from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.victoria.ca/city-government/mayor-council/members-council"


class VictoriaPersonScraper(CanadianScraper):
    def scrape(self):
        seat_number = 1
        page = self.lxmlize(COUNCIL_PAGE)

        councillors = page.xpath(
            '//article[@class="node node--type-councillor node--view-mode-list-item list-item flex fd-r fd-c-mq-m g-32"]'
        )
        assert len(councillors), "No councillors found"
        for councillor in councillors:
            role, name = councillor.xpath(".//h3/a/span")[0].text_content().split(" ", 1)
            photo = councillor.xpath(".//img/@src")[0]
            email = self.get_email(councillor)
            phone = self.get_phone(councillor)
            url = councillor.xpath(".//h3/a/@href")[0]

            district = f"Victoria (seat {seat_number})"
            seat_number += 1

            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.image = photo
            p.add_contact("email", email)
            p.add_contact("voice", phone, "legislature")
            p.add_source(COUNCIL_PAGE)
            p.add_source(url)

            yield p

        mayor_url = page.xpath(
            '//ul[@class="menu menu--level-0"]//a[contains(., "Mayor") and not(contains(., "Council"))]/@href'
        )[0]
        page = self.lxmlize(mayor_url)
        role, name = page.xpath("//h1/span")[0].text_content().split(" ", 1)
        photo = councillor.xpath('//div[@class="field__item"]/img/@src')[0]
        email = self.get_email(page)
        phone = self.get_phone(page)
        p = Person(primary_org="legislature", name=name, district="Victoria", role=role)
        p.image = photo
        p.add_contact("email", email)
        p.add_contact("voice", phone, "legislature")
        p.add_source(mayor_url)

        yield p
