from __future__ import unicode_literals
from utils import CanadianScraper, CanadianPerson as Person

COUNCIL_PAGE = 'http://www.wellesley.ca/council/councillors/?q=council/councillors'


def post_number(name):
    return {
        'Ward One': 'Ward 1',
        'Ward Two': 'Ward 2',
        'Ward Three': 'Ward 3',
        'Ward Four': 'Ward 4'
    }[name]


class WellesleyPersonScraper(CanadianScraper):

    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        councillors = page.xpath('//div[@class="img_four"][1]/div[1]')
        councillors = councillors + page.xpath('//div[@class="img_four"][2]/div')
        for councillor_elem in councillors:
            name, position = councillor_elem.xpath('string(./p/strong)').split(',')
            position = position.strip()
            if ' ' in position:
                position, district = position.split(' ', 1)
                district = post_number(district)
            else:
                district = 'Wellesley'
            addr = '\n'.join(addr_str.strip() for addr_str in
                             councillor_elem.xpath('./p/text()')).strip()
            phone = councillor_elem.xpath('string(.//a[starts-with(@href, "tel:")])')
            email = councillor_elem.xpath('string(.//a[starts-with(@href, "mailto:")])')
            image = councillor_elem.xpath('.//img[1]/@src')[0]
            p = Person(primary_org='legislature', name=name, district=district, role=position, image=image)
            p.add_source(COUNCIL_PAGE)
            p.add_contact('address', addr, 'legislature')
            p.add_contact('voice', phone, 'legislature')
            p.add_contact('email', email)
            yield p
