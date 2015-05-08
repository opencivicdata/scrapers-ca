from __future__ import unicode_literals
from utils import CanadianScraper, CanadianPerson as Person

import json
import re


class CanadaCandidatesPersonScraper(CanadianScraper):

    def scrape(self):
        # http://www.blocquebecois.org/equipe-2015/circonscriptions/candidats/

        url = 'http://www.conservative.ca/wp-content/themes/conservative/scripts/candidates.json'
        for nodes in json.loads(self.get(url).text).values():
            for node in nodes:
                name = node['candidate']
                district = node['district']

                p = Person(primary_org='legislature', name=name, district=district, role='candidate', party='Conservative')
                p.image = 'http://www.conservative.ca/media/candidates/{}'.format(node['image'])

                p.add_source(url)
                yield p

        url = 'http://www.greenparty.ca/en/candidates'
        for node in self.lxmlize(url).xpath('//div[@class="candidate-card"]'):
            name = node.xpath('./div[@class="candidate-name"]//text()')[0]
            district = node.xpath('./@data-target')[0][5:]  # node.xpath('./div[@class="riding-name"]//text()')[0]

            p = Person(primary_org='legislature', name=name, district=district, role='candidate', party='Green Party')
            p.image = node.xpath('./img[@typeof="foaf:Image"]/@src')[0]  # print quality also available

            p.add_contact('email', self.get_email(node))

            p.add_link(node.xpath('.//div[@class="margin-bottom-gutter"]/a[contains(@href,"http")]/@href')[0])
            self.add_links(p, node)

            p.add_source(url)
            yield p

        url = 'https://www.liberal.ca/candidates/'
        for node in self.lxmlize(url).xpath('//ul[@id="candidates"]/li'):
            name = node.xpath('./h2/text()')[0]
            district = node.xpath('./@data-riding-riding_id')[0]  # node.xpath('./@data-riding-name')[0]

            p = Person(primary_org='legislature', name=name, district=district, role='candidate', party='Liberal')
            p.image = node.xpath('./@data-photo-url')[0][4:-1]

            if node.xpath('./@class[contains(.,"candidate-female")]'):
                p.gender = 'female'
            elif node.xpath('./@class[contains(.,"candidate-male")]'):
                p.gender = 'male'

            p.add_link(node.xpath('.//a[contains(@href,".liberal.ca")]/@href')[0])
            self.add_links(p, node)

            p.add_source(url)
            yield p

        url = 'http://www.ndp.ca/candidates'
        for node in self.lxmlize(url, encoding='utf-8').xpath('//div[@class="candidate-holder"]'):
            image = node.xpath('.//div/@data-img')[0]

            name = node.xpath('.//div[@class="candidate-name"]//text()')[0]
            district = re.search(r'\d{5}', image).group(0)  # node.xpath('.//span[@class="candidate-riding-name"]/text()')[0]

            p = Person(primary_org='legislature', name=name, district=district, role='candidate', party='NDP')
            p.image = image

            if node.xpath('.//div[contains(@class,"placeholder-f")]'):
                p.gender = 'female'
            elif node.xpath('.//div[contains(@class,"placeholder-m")]'):
                p.gender = 'male'

            twitter = node.xpath('.//a[@class="candidate-twitter"]/@href')
            if twitter:
                p.add_link(twitter[0])
            facebook = node.xpath('.//a[@class="candidate-facebook"]/@href')
            if facebook:
                p.add_link(facebook[0])

            p.add_source(url)
            yield p

    def add_links(self, p, node):
        for substring in ('facebook.com', 'instagram.com', 'twitter.com', 'youtube.com'):
            link = self.get_link(node, substring, error=False)
            if link:
                p.add_link(link)
