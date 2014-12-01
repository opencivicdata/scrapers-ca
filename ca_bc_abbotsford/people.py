from __future__ import unicode_literals
from utils import CanadianScraper, CanadianPerson as Person

COUNCIL_PAGE = 'http://www.abbotsford.ca/mayorcouncil/city_council/email_mayor_and_council.htm'

MAYOR_URL = 'http://www.abbotsford.ca/mayorcouncil/city_council/mayor_banman.htm'


class AbbotsfordPersonScraper(CanadianScraper):

    def scrape(self):
        councillor_seat_number = 1

        page = self.lxmlize(COUNCIL_PAGE)
        councillor_links = page.xpath('//li[@id="pageid2117"]/ul/li/a')[2:10]
        for link in councillor_links:
            if not link.text.startswith('Councillor'):
                continue
            url = link.attrib['href']
            page = self.lxmlize(url)
            mail_link = page.xpath('//a[@title]')[0]
            name = mail_link.attrib['title']
            email = mail_link.attrib['href'][len('mailto:'):]
            photo_url = page.xpath('//div[@class="pageContent"]//img[@align="right"]/@src')[0]

            district = 'Abbotsford (seat %d)' % councillor_seat_number
            councillor_seat_number += 1

            p = Person(primary_org='legislature', name=name, district=district, role='Councillor', image=photo_url)
            p.add_source(COUNCIL_PAGE)
            p.add_source(url)
            p.add_contact('email', email)
            yield p

        page = self.lxmlize(MAYOR_URL)
        name = page.xpath('string(//h1)').split(' ', 1)[1]
        photo_url = page.xpath('//img[@hspace=10]/@src')[0]
        # email is hidden behind a form
        p = Person(primary_org='legislature', name=name, district='Abbotsford', role='Mayor', image=photo_url)
        p.add_source(MAYOR_URL)
        yield p
