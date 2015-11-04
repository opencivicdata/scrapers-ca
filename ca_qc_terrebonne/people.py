from __future__ import unicode_literals
from utils import CanadianScraper, CanadianPerson as Person

COUNCIL_PAGE = 'http://www.ville.terrebonne.qc.ca/fr/10/Conseil_municipal'


class TerrebonnePersonScraper(CanadianScraper):

    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE, 'utf-8')
        for councillor_elem in page.xpath('//div[@class="member-box member-box--gray"]'):
            name = councillor_elem.xpath('.//div[@class="fiche__name"]/text()')[0]
            district = councillor_elem.xpath('.//div[@class="fiche__category"]/text()')[0]
            phone = councillor_elem.xpath('.//div[@class="fiche__social"]/span/text()')[0].split('T')[1]
            email_mailto = councillor_elem.xpath('.//div[@class="fiche__social"]/a[contains(@href, "mailto")]/@href')
            photo_url = councillor_elem.xpath('.//img')[0].attrib['src']

            p = Person(primary_org='legislature', name=name, district=district, role='Conseiller',
                       image=photo_url)
            p.add_source(COUNCIL_PAGE)
            p.add_contact('voice', phone, 'legislature')
            if email_mailto:
                email = email_mailto[0].split('mailto:')[1]
                p.add_contact('email', email)
            yield p

        mayor_elem = page.xpath('//div[@class="member-box member-box--main"]')[0]
        name = mayor_elem.xpath('.//div[@class="fiche__name"]/text()')[0]
        phone = mayor_elem.xpath('.//div[@class="fiche__social"]/span/text()')[0].split('T')[1]
        email_mailto = mayor_elem.xpath('.//div[@class="fiche__social"]/a[contains(@href, "mailto")]/@href')
        photo_url = councillor_elem.xpath('.//img')[0].attrib['src']
        p = Person(primary_org='legislature', name=name, district='Terrebonne', role='Maire',
                   image=photo_url)
        p.add_source(COUNCIL_PAGE)
        p.add_contact('voice', phone, 'legislature')
        if email_mailto:
            email = email_mailto[0].split('mailto:')[1]
            p.add_contact('email', email)
        yield p
