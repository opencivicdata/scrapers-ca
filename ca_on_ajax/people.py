from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.ajax.ca/en/inside-townhall/council-members.aspx"


class AjaxPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        councillors = page.xpath('//table[@class="councilTable"]')
        assert len(councillors), "No councillors found"
        for councillor in councillors:
            image = councillor.xpath(".//@src")[0]
            alt = councillor.xpath(".//tr/td[1]/p[1]/img/@alt")[0]

            if "Mayor" in alt:
                name = alt
                district = "Ajax"
                role = "Mayor"
            else:
                name, rest = alt.split(" - ", 1)
                district = rest.split("Councillor ", 1)[-1].strip()
                role = rest.split("Ward ", 1)[0].strip()

            cell = councillor.xpath('.//p[contains(.,"Cel")]/text()')[0].replace("Cell: ", "")
            if councillor.xpath('.//p[contains(.,"Tel")]/text()'):
                voice = councillor.xpath('.//p[contains(.,"Tel")]/text()')[1].replace(" Tel: ", "")
            email = self.get_email(councillor)

            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)
            p.image = image

            if cell:
                p.add_contact("cell", cell, "legislature")
            if voice:
                p.add_contact("voice", voice, "legislature")
            if email:
                p.add_contact("email", email)
            yield p
