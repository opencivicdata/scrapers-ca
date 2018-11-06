from utils import CanadianScraper, CanadianPerson as Person

COUNCIL_PAGE = 'http://www.coquitlam.ca/city-hall/mayor-and-council/mayor-and-council.aspx'


class CoquitlamPersonScraper(CanadianScraper):
    def scrape(self):
        councillor_seat_number = 1

        page = self.lxmlize(COUNCIL_PAGE)
        councillors = page.xpath('//div[@id="subnav"]//a[@class="L4"]')
        assert len(councillors), 'No councillors found'
        for person_link in councillors:
            role, name = person_link.text_content().split(' ', 1)
            url = person_link.attrib['href']
            page = self.lxmlize(url)
            image = page.xpath('//img[@class="img-right"]/@src')
            email = self.get_email(page)

            if role == 'Mayor':
                district = 'Coquitlam'
            else:
                district = 'Coquitlam (seat {})'.format(councillor_seat_number)
                councillor_seat_number += 1

            p = Person(primary_org='legislature', name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)
            p.add_source(url)

            if image:
                p.image = image[0]

            p.add_contact('email', email)

            yield p
