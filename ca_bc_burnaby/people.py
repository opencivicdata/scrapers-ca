from utils import CanadianScraper, CanadianPerson as Person

COUNCIL_PAGE = 'https://www.burnaby.ca/Our-City-Hall/Mayor---Council/Council-Profiles.html'


class BurnabyPersonScraper(CanadianScraper):
    def scrape(self):
        councillor_seat_number = 1

        page = self.lxmlize(COUNCIL_PAGE)
        councillors = page.xpath('//h4/a/@href')
        assert len(councillors), 'No councillors found'
        for person_url in councillors:
            page = self.lxmlize(person_url)

            role, name = page.xpath('//title//text()')[0].split(' ', 1)
            photo_url = page.xpath('//div[@id="content"]//img[@style]/@src')[0]

            content_node = page.xpath('//div[@id="content"]')[0]

            email = self.get_email(content_node)

            phone = self.get_phone(content_node, area_codes=[604, 778])

            if role == 'Mayor':
                district = 'Burnaby'
            else:
                district = 'Burnaby (seat {})'.format(councillor_seat_number)
                councillor_seat_number += 1

            p = Person(primary_org='legislature', name=name, district=district, role=role, image=photo_url)
            p.add_source(COUNCIL_PAGE)
            p.add_source(person_url)
            if email:
                p.add_contact('email', email)
            if phone:
                p.add_contact('voice', phone, 'legislature')
            yield p
