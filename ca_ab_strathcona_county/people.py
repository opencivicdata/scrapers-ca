# coding: utf-8
from __future__ import unicode_literals

import re

from six.moves.urllib.parse import urljoin

from utils import CanadianScraper, CanadianPerson as Person

COUNCIL_PAGE = 'http://www.strathcona.ca/local-government/mayor-councillors/councillors/'

MAYOR_PAGE = 'http://www.strathcona.ca/local-government/mayor-councillors/mayor/'


class StrathconaCountyPersonScraper(CanadianScraper):

    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)
        councillor_urls = page.xpath('//div[@class="usercontent"]//td/a/@href')
        for url in councillor_urls:
            yield self.councillor_data(url)
        yield self.mayor_data(MAYOR_PAGE)

    def councillor_data(self, url):
        page = self.lxmlize(url)
        name, ward = re.match('Councillor (.+) - (.+)',
                              page.xpath('string(//h1)')).groups()
        content_node = page.xpath('//div[@class="usercontent"]')[0]
        photo_url_rel = content_node.xpath('string(.//img[1]/@src)')
        photo_url = urljoin(COUNCIL_PAGE, photo_url_rel)
        email = content_node.xpath('string(.//a/text()[contains(., "@")])')
        phone = content_node.xpath('string(.//strong[contains(., "Phone")]/'
                                   'following-sibling::text()[1])').strip()

        p = Person(primary_org='legislature', name=name, district=ward, role='Councillor')
        p.add_source(COUNCIL_PAGE)
        p.add_source(url)
        if phone:
            p.add_contact('voice', phone, 'legislature')
        p.add_contact('email', email)
        p.image = photo_url
        return p

    def mayor_data(self, url):
        page = self.lxmlize(url)
        name = page.xpath('string(//h1)').split('-')[1]
        content_node = page.xpath('//div[@class="usercontent"]')[0]
        photo_url = urljoin(url, content_node.xpath('string(.//img[1]/@src)'))
        email = content_node.xpath('string(.//a/text()[contains(., "@")])')
        phone = content_node.xpath('string(.//strong[contains(., "Phone")]/'
                                   'following-sibling::text()[1])').strip()

        p = Person(primary_org='legislature', name=name, district='Strathcona County', role='Mayor')
        p.add_source(COUNCIL_PAGE)
        p.add_source(url)
        p.add_contact('voice', phone, 'legislature')
        p.add_contact('email', email)
        p.image = photo_url
        return p
