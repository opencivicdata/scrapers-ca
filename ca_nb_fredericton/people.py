from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "http://www.fredericton.ca/en/city-hall/city-council-committees/mayor-council"


class FrederictonPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        councillors = page.xpath('//div[contains(@class, "view-people")]//div[contains(@class, "views-row")]')
        assert len(councillors), "No councillors found"
        for councillor in councillors:
            name = councillor.xpath('.//div[@property="dc:title"]//text()')[0]
            paras = councillor.xpath('.//div[contains(@class, "field-name-field-sub-title")]//p/text()')

            if paras[0] == "Mayor":
                district = "Fredericton"
                role = "Mayor"
            else:
                if paras[0] == "Deputy Mayor":
                    index = 1
                else:
                    index = 0

                district = paras[index].replace("\xa0", " ").split(", ", 1)[1]
                role = "Councillor"

            url = councillor.xpath(".//@href")[0]
            page = self.lxmlize(url)

            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)
            p.add_source(url)

            p.image = councillor.xpath('.//img[@typeof="foaf:Image"]/@src')[0]
            p.add_contact("email", self.get_email(page))
            p.add_contact("voice", self.get_phone(page, area_codes=[506]), "legislature")

            yield p
