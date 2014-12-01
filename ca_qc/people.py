# coding: utf-8
from __future__ import unicode_literals
from utils import CanadianScraper, CanadianPerson as Person

COUNCIL_PAGE = 'http://www.assnat.qc.ca/fr/deputes/index.html'


class QuebecPersonScraper(CanadianScraper):

    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)
        for row in page.xpath('//*[@id="ListeDeputes"]/tbody/tr'):
            name_comma, division = [cell.xpath('string(.)') for cell in row[:2]]
            name = ' '.join(reversed(name_comma.strip().split(',')))
            party = row[2].text_content()
            email = row[3].xpath('string(.//a/@href)').replace('mailto:', '')
            detail_url = row[0][0].attrib['href']
            detail_page = self.lxmlize(detail_url)
            photo_url = detail_page.xpath('//img[@class="photoDepute"]/@src')[0]
            division = division.replace('–', '—')  # n-dash, m-dash
            p = Person(primary_org='legislature', name=name, district=division, role='MNA',
                       party=party, image=photo_url)
            p.add_source(COUNCIL_PAGE)
            p.add_source(detail_url)
            if email:  # Premier may not have email.
                p.add_contact('email', email)
            yield p
