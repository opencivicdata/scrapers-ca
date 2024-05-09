from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.fredericton.ca/en/your-government/mayor-council"


class FrederictonPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        councillors = page.xpath('//div[contains(@class, "view view-councillor view-id-councillor view-display-id-block_1 js-view-dom-id-60ab7690fd8036f968c4406929bf5bec3a3f03554afaf4ff046cb5487dadf8da contextual-region")]//div[contains(@class, "views-row")]')
        assert len(councillors), "No councillors found"
        for councillor in councillors:
            name = councillor.xpath('.//h3/a')[0].text_content()
            text = councillor.xpath('.//div[@class="views-field views-field-field-councillor-title"]/div')[0].text_content()
            ward_start = text.find("Ward")
            if ward_start+1:
                district = text[ward_start:ward_start+7].strip()
                role = "Councillor"
            else:
                district = "Fredericton"
                role = "Mayor"

            url = councillor.xpath(".//@href")[0]
            page = self.lxmlize(url)

            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)
            p.add_source(url)

            p.image = councillor.xpath('.//img[@typeof="foaf:Image"]/@src')[0]
            p.add_contact("email", self.get_email(page))
            p.add_contact("voice", self.get_phone(page, area_codes=[506]), "legislature")

            yield p
