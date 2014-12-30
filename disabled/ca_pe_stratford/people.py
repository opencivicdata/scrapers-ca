from __future__ import unicode_literals
from utils import CanadianScraper, CanadianPerson as Person

import re
from collections import defaultdict

COUNCIL_PAGE = 'http://www.townofstratford.ca/town-hall/government/town-council/'


class StratfordPersonScraper(CanadianScraper):
    def scrape(self):
        seat_numbers = defaultdict(int)

        page = self.lxmlize(COUNCIL_PAGE, user_agent='Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)')

        yield self.scrape_mayor(page)

        councillors = page.xpath('//div[@id="street-container"]//strong[contains(text(), "Councillor")]/parent::p|//div[@id="street-container"]//b[contains(text(), "Councillor")]/parent::p')
        for councillor in councillors:

            name = councillor.xpath('./strong/text()|./b/text()')[0].replace('Councillor', '').strip()
            post = re.findall('(?<=Ward \d, ).*', councillor.text_content())[0].strip()

            seat_numbers[post] += 1
            post = '%s (seat %d)' % (post, seat_numbers[post])

            p = Person(primary_org='legislature', name=name, district=post, role='Councillor')
            p.add_source(COUNCIL_PAGE)

            p.image = councillor.xpath('.//img/@src')[0]

            phone = re.findall(r'Phone(.*)', councillor.text_content())
            node = councillor
            while not phone:
                node = node.xpath('./following-sibling::p')[1]
                phone = re.findall(r'Phone(.*)', node.text_content())
            phone = phone[0].strip()

            email = self.get_email(councillor, error=False)
            if not email:
                email = self.get_email(councillor, './following-sibling::p')

            if len(re.sub(r'\D', '', phone)) == 7:
                phone = '902-%s' % phone
            p.add_contact('voice', phone, 'legislature')
            p.add_contact('email', email)

            yield p

    def scrape_mayor(self, page):
        info = page.xpath('//div[@class="entry-content"]/p')[:4]
        name = info[0].text_content().replace('Mayor', '')
        email = self.get_email(info[2])
        phone = info[3].text_content().replace('Phone ', '')

        p = Person(primary_org='legislature', name=name, district='Stratford', role='Mayor')
        p.add_source(COUNCIL_PAGE)
        p.image = page.xpath('//div[@class="entry-content"]/p/a/img/@src')[0]
        p.add_contact('email', email)
        if len(re.sub(r'\D', '', phone)) == 7:
            phone = '902-%s' % phone
        p.add_contact('voice', phone, 'legislature')
        return p
