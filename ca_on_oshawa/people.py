from utils import CanadianScraper, CanadianPerson as Person

COUNCIL_PAGE = 'http://www.oshawa.ca/city-hall/city-council-members.asp'


class OshawaPersonScraper(CanadianScraper):

    def scrape(self):
        councillor_seat_number = 1
        regional_councillor_seat_number = 1

        page = self.lxmlize(COUNCIL_PAGE)
        councillors = page.xpath('//table//td')

        assert len(councillors), 'No councillors found'
        for councillor in councillors:
            if councillor.xpath('./p[1]/text()'):
                name, role = councillor.xpath('./p[1]/text()')
            else:
                name, role = councillor.xpath('./span[1]/text()')

            role = role.strip()

            if role == 'City Councillor':
                role = 'Councillor'
                district = 'Oshawa (seat {})'.format(councillor_seat_number)
                councillor_seat_number += 1
            elif role == 'Regional and City Councillor':
                role = 'Regional Councillor'
                district = 'Oshawa (seat {})'.format(regional_councillor_seat_number)
                regional_councillor_seat_number += 1
            else:
                district = 'Oshawa'

            photo_url = councillor.xpath('./p/img/@src')[0]
            phone = self.get_phone(councillor.xpath('./p[contains(.//text(), "Phone")]')[0], area_codes=[905])

            p = Person(primary_org='legislature', name=name, district=district, role=role, image=photo_url)
            p.add_source(COUNCIL_PAGE)
            p.add_contact('voice', phone, 'legislature')
            p.add_contact('email', self.get_email(councillor))
            yield p
