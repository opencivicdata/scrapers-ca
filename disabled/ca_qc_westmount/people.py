from utils import CanadianScraper, CanadianPerson as Person

COUNCIL_PAGE = 'http://westmount.org/conseil/conseil-de-la-ville/'


class WestmountPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        councillors = page.xpath('//div[@class="member-container"]')
        for councillor in councillors:
            name = councillor.xpath('.//h3')[0].text_content()
            role = councillor.xpath('.//div[@class="member-position"]')[0].text_content()
            if 'Maire' in role:
                role = 'Maire'
                district = 'Westmount'
            else:
                role = 'Conseiller'
                district = councillor.xpath('.//div[@class="entry-content"]/text()')[0]

            p = Person(primary_org='legislature', name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)

            p.image = councillor.xpath('.//a[@title="Photo pour la presse"]/@href')[0]
            p.add_contact('email', self.get_email(councillor))

            yield p
