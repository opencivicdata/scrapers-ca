from __future__ import unicode_literals
from utils import CanadianScraper, CanadianPerson as Person

COUNCIL_PAGE = 'http://ville.saguenay.ca/fr/administration-municipale/conseils-municipaux-et-darrondissement/membres-des-conseils'


class SaguenayPersonScraper(CanadianScraper):

    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        mayor = page.xpath('//div[@class="box"]/p/text()')
        m_name = mayor[0].strip().split('.')[1].strip()
        m_phone = mayor[1].strip().split(':')[1].strip()

        m = Person(primary_org='legislature', name=m_name, district='Saguenay', role='Maire')
        m.add_source(COUNCIL_PAGE)
        m.add_contact('voice', m_phone, 'legislature')

        yield m

        councillors = page.xpath('//div[@class="box"]//div')
        for councillor in councillors:
            district = councillor.xpath('./h3')[0].text_content().replace('#', '')
            name = councillor.xpath('.//p/text()')[0].encode('latin-1').decode('utf-8')
            name = name.replace('M. ', '').replace('Mme ', '').strip()
            phone = councillor.xpath('.//p/text()')[1].split(':')[1].strip().replace(' ', '-')
            email = self.get_email(councillor)

            p = Person(primary_org='legislature', name=name, district=district, role='Conseiller')
            p.add_source(COUNCIL_PAGE)

            p.add_contact('voice', phone, 'legislature')
            p.add_contact('email', email)
            yield p
