from utils import CanadianScraper, CanadianPerson as Person

COUNCIL_PAGE = 'http://ville.ddo.qc.ca/en/my-municipality/members-council'


class DollardDesOrmeauxPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        general_contacts = page.xpath('//h3/following-sibling::p/text()')
        general_phone = general_contacts[0]
        general_fax = general_contacts[1]

        councillors = page.xpath('//div[@class="membre-conseil-single"]')
        assert len(councillors), 'No councillors found'
        for councillor in councillors:
            name = councillor.xpath('./div[@class="membre-conseil-nom"]/text()')[0]
            name = ' '.join(reversed(name.split(', ')))
            district = councillor.xpath('./div[@class="membre-conseil-poste"]/text()')[0]
            email = self.get_email(councillor)

            if district == 'Mayor':
                district = 'Dollard-Des Ormeaux'
                role = 'Maire'
            else:
                role = 'Conseiller'

            p = Person(primary_org='legislature', name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)
            p.image = councillor.xpath('./div[@class="membre-conseil-photo"]//@src')[0]

            p.add_contact('email', email)
            p.add_contact('voice', general_phone, 'legislature')
            p.add_contact('fax', general_fax, 'legislature')

            yield p
