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

        yield self.scrape_mayor(page.xpath('//div[@class="img_four"][1]/div[1]')[0])

        councillors = page.xpath('//div[@class="img_four"][2]/div')
        assert len(councillors), 'No councillors found'
        for councillor_elem in councillors:
            name, position = councillor_elem.xpath('string(./p/strong)').split(',')  # allow string()
            position = position.strip()
            position, district = position.split(' ', 1)
            district = post_number(district)
            addr = '\n'.join(addr_str.strip() for addr_str in
                             councillor_elem.xpath('./p/text()')).strip()
            phone = councillor_elem.xpath('.//a[starts-with(@href, "tel:")]//text()')[0]
            image = councillor_elem.xpath('.//img[1]/@src')[0]
            p = Person(primary_org='legislature', name=name, district=district, role=position, image=image)
            p.add_source(COUNCIL_PAGE)
            p.add_contact('address', addr, 'legislature')
            p.add_contact('voice', phone, 'legislature')
            yield p

    def scrape_mayor(self, mayor_node):
        name, position = mayor_node.xpath('string(./p/strong)').split(',')  # allow string()
        position = position.strip()
        district = 'Wellesley'
        addr = '\n'.join(addr_str.strip() for addr_str in
                         mayor_node.xpath('./p/text()')).strip()
        phone = mayor_node.xpath('.//a[starts-with(@href, "tel:")]//text()')[0]
        image = mayor_node.xpath('.//img[1]/@src')[0]
        p = Person(primary_org='legislature', name=name, district=district, role=position, image=image)
        p.add_source(COUNCIL_PAGE)
        p.add_contact('address', addr, 'legislature')
        p.add_contact('voice', phone, 'legislature')
        return p
