from utils import CanadianScraper, CanadianPerson as Person

COUNCIL_PAGE = 'http://www.ville.sherbrooke.qc.ca/mairie-et-vie-democratique/conseil-municipal/elus-municipaux/'


class SherbrookePersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        councillors = page.xpath('//div[@id="c2087"]//a')
        assert len(councillors), 'No councillors found'
        for councillor in councillors:
            name = councillor.text_content()
            url = councillor.attrib['href']
            page = self.lxmlize(url)
            if 'Maire' in page.xpath('//h2/text()')[0]:
                district = 'Sherbrooke'
                role = 'Maire'
            else:
                district = page.xpath('//div[@class="csc-default"]//a[@target="_blank"]/text()')[0].replace('district', '').replace('Domaine Howard', 'Domaine-Howard').strip()
                role = 'Conseiller'
            if district in ('de Brompton', 'de Lennoxville'):
                district = district.replace('de ', '')
            p = Person(primary_org='legislature', name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)
            p.add_source(url)
            p.image = page.xpath('//div[@class="csc-textpic-image csc-textpic-last"]//img/@src')[0]
            parts = page.xpath('//li[contains(text(), "phone")]/text()')[0].split(':')
            note = parts[0]
            phone = parts[1]
            p.add_contact(note, phone, note)
            email = self.get_email(page)
            if email:
                p.add_contact('email', email)
            if district == 'Brompton':
                p._related[0].extras['boundary_url'] = '/boundaries/sherbrooke-boroughs/brompton/'
            elif district == 'Lennoxville':
                p._related[0].extras['boundary_url'] = '/boundaries/sherbrooke-boroughs/lennoxville/'
            yield p
