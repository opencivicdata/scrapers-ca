from __future__ import unicode_literals
from utils import CanadianScraper, CanadianPerson as Person

from six.moves.urllib.parse import urljoin

COUNCIL_PAGE = 'http://www.citywindsor.ca/mayorandcouncil/City-Councillors/Pages/City-Councillors.aspx'
MAYOR_PAGE = 'http://www.citywindsor.ca/mayorandcouncil/Pages/Biography-of-the-Mayor.aspx'


class WindsorPersonScraper(CanadianScraper):

    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        councillor_links = page.xpath('//span[@class="textimagetype"]//a[contains(text(), "- Ward")]')
        for councillor_link in councillor_links:
            name, district = councillor_link.text.split(' - ')
            cpage_url = councillor_link.attrib['href']
            cpage = self.lxmlize(cpage_url)
            p = Person(primary_org='legislature', name=name, district=district, role='Councillor')
            p.add_source(COUNCIL_PAGE)
            p.add_source(cpage_url)

            email = cpage.xpath('//a[contains(@href, "@")]//text()')[0]
            p.add_contact('email', email)

            phone = cpage.xpath('string(//text()[contains(., "Phone")])').split(':')[1]
            p.add_contact('voice', phone, 'legislature')

            img_url_rel = cpage.xpath('(//span/img)[1]/@src')[0]
            img_url = urljoin(cpage_url, img_url_rel)
            p.image = img_url

            yield p

        page = self.lxmlize(MAYOR_PAGE)
        name = ' '.join(page.xpath('//p[contains(text(), "is married to")]/text()')[0].split()[:2])
        address = ' '.join(page.xpath('//p[contains(text(), "Mayor\'s Office")]/text()')[1:])
        phone, fax = page.xpath('//p[contains(text(), "Phone:")]/text()')[:-1]
        phone = phone.strip().replace('(', '').replace(') ', '-')
        fax = fax.strip().replace('(', '').replace(') ', '-').split(':')[1]
        email = page.xpath('//a[contains(@href, "mailto:")]/text()')[0]

        p = Person(primary_org='legislature', name=name, district='Windsor', role='Mayor')
        p.add_source(MAYOR_PAGE)
        p.add_contact('address', address, 'legislature')
        p.add_contact('voice', phone, 'legislature')
        p.add_contact('fax', fax, 'legislature')
        p.add_contact('email', email)
        p.image = page.xpath('//div[@class="sectioning"]//img[contains(@title, "Mayor")]/@src')[0]
        yield p
