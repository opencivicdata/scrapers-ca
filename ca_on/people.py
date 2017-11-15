# coding: utf-8
from utils import CanadianScraper, CanadianPerson as Person

COUNCIL_PAGE = 'http://www.ontla.on.ca/web/members/member_addresses.do'


class OntarioPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)
        members = page.xpath('//div[@class="addressblock"]')
        assert len(members), 'No members found'
        for block in members:
            if block.xpath('.//div[@class="vacant-seat"]'):
                continue

            name_elem = block.xpath('.//a[@class="mpp"]')[0]
            name = ' '.join(name_elem.text.split())

            riding = block.xpath('.//div[@class="riding"]//text()')[0].strip().replace('--', '\u2014')
            district = riding.replace('Chatham—Kent', 'Chatham-Kent')  # m-dash to hyphen
            mpp_url = name_elem.attrib['href']

            mpp_page = self.lxmlize(mpp_url)
            if mpp_page.xpath('//title[contains(text(),"Past & Present MPPs")]'):  # past MPP
                continue

            image = mpp_page.xpath('//img[@class="mppimg"]/@src')
            party = mpp_page.xpath('//div[@class="mppinfoblock"]/p[last()]/text()')[0].strip()

            p = Person(primary_org='legislature', name=name, district=district, role='MPP', party=party)
            if image:
                p.image = image[0]
            p.add_source(COUNCIL_PAGE)
            p.add_source(mpp_url)

            email = block.xpath('.//div[@class="email"]')
            if email:
                p.add_contact('email', self.get_email(email[0]))

            phone = block.xpath('.//div[@class="phone"]//text()')
            if phone:
                p.add_contact('voice', phone[0], 'legislature')

            yield p
