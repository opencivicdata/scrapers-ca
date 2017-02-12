from __future__ import unicode_literals
from utils import CanadianScraper, CanadianPerson as Person

import re

from six.moves.urllib.parse import urljoin

COUNCIL_PAGE = 'http://winnipeg.ca/council/'


class WinnipegPersonScraper(CanadianScraper):

    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE, 'utf-8')
        councillors = page.xpath('//table[@class="council-table"]//td[not(@colspan)]')
        assert len(councillors), 'No councillors found'
        for node in councillors:
            url = urljoin(COUNCIL_PAGE, node.xpath('.//a/@href')[0])
            text = ' '.join(node.xpath('.//a//text()'))
            ward = re.search('([A-Z].+) Ward', text).group(1)
            ward = ward.replace(' – ', '—').replace(' - ', '—')  # n-dash, m-dash, hyphen, m-dash
            ward = ward.replace('St. Norbert', 'St Norbert')  # to match ocd-division-ids
            name = ' '.join(node.xpath('.//span[@class="k80B"][1]/text()'))
            yield self.councillor_data(url, name, ward)

        mayor_node = page.xpath('//td[@colspan]')[0]
        mayor_name = mayor_node.xpath('.//p[@class="k90B"][1]/text()')[0].replace('Mayor ', '')
        mayor_photo_url = mayor_node.xpath('.//img/@src')[0]
        m = Person(primary_org='legislature', name=mayor_name, district='Winnipeg', role='Mayor')
        m.add_source(COUNCIL_PAGE)
        # @see http://www.winnipeg.ca/interhom/mayor/MayorForm.asp?Recipient=CLK-MayorWebMail
        m.add_contact('email', 'CLK-MayorWebMail@winnipeg.ca')  # hardcoded
        m.image = mayor_photo_url
        yield m

    def councillor_data(self, url, name, ward):
        page = self.lxmlize(url)
        # email is, sadly, a form
        photo_url = urljoin(url, page.xpath('//img[@class="bio_pic"]/@src')[0])
        phone = page.xpath('//td[contains(., "Phone")]/following-sibling::td//text()')[0]
        email = re.search('=([^&]+)', page.xpath('//tr[contains(., "Email")]//a/@href')[0]).group(1) + '@winnipeg.ca'

        p = Person(primary_org='legislature', name=name, district=ward, role='Councillor')
        p.add_source(COUNCIL_PAGE)
        p.add_source(url)
        p.add_contact('email', email)
        p.add_contact('voice', phone, 'legislature')
        p.image = photo_url

        return p
