from utils import CanadianScraper, CanadianPerson as Person

COUNCIL_PAGE = 'https://westmount.org/conseil-municipal/'


class WestmountPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        councillors = page.xpath('//div[contains(@class, "vc_row")][./div[contains(@class, "vc_col-sm-4")]]')
        assert len(councillors), 'No councillors found'
        for councillor in councillors:
            name = councillor.xpath('.//h4/text()')[0]
            role = councillor.xpath('.//strong//text()')

            if role and 'Maire' in role[0]:
                role = 'Maire'
                district = 'Westmount'
            else:
                role = 'Conseiller'
                district = councillor.xpath('.//li//text()')[0]

            p = Person(primary_org='legislature', name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)

            p.image = councillor.xpath('.//@src')[0]
            p.add_contact('voice', self.get_phone(councillor), 'legislature')
            p.add_contact('email', self.get_email(councillor))

            yield p
