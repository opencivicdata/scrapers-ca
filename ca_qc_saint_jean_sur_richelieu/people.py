from utils import CanadianScraper, CanadianPerson as Person, clean_string
import re
from urllib.parse import urljoin

COUNCIL_PAGE = 'https://sjsr.ca/conseil-municipal/'

class SaintJeanSurRichelieuPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE,encoding='utf-8')

        councillors = page.xpath('//div[contains(@class,"fl-module-content fl-node-content")]/div[@class="fl-rich-text"]//a')
        assert len(councillors), 'No councillors found'
        for councillor in councillors:

            name= councillor.xpath('.//text()')[0]
            url = councillor.xpath('./@href')[0]
            if name[0]:
                ward = 'Saint-Jean-sur-Richelieu'
                role = 'Maire'
            else:
                role = councillor.xpath('.//p[data-swp-font-size="16px"]/br/text()')[0]
                ward = councillor.xpath('.//p[data-swp-font-size="16px"]/br/br/text()')[0]

            yield self.councillor_data(url, name, ward, role)

    def councillor_data(self, url, name, ward, role):
            node = self.lxmlize(url)
            photo_url_rel = node.xpath('//div[@class="fl-photo-content fl-photo-img-jpg"]//img/@src')[0]
            photo_url = urljoin(url, photo_url_rel)
            
            p = Person(primary_org='legislature', name=name, district=ward, role=role)
            p.add_source(COUNCIL_PAGE)
            p.add_source(url)
            p.image = photo_url

            if node.xpath('//div[contains(@class,"fl-module-content fl-node-content")]/div[@class="fl-rich-text"]/p[2]/strong//text()'):
                p.add_contact('voice', node.xpath('//div[contains(@class,"fl-module-content fl-node-content")]/div[@class="fl-rich-text"]/p[2]/strong//text()')[0],'legislature')

            yield p

