from __future__ import unicode_literals
from pupa.scrape import Scraper, Organization

import re

from utils import CanadianScraper, CanadianPerson as Person

COUNCIL_PAGE = 'http://www2.gnb.ca/content/gnb/en/departments/elg/local_government/content/community_profiles.html'
org_types = [' City Council', ' Town Council', ' Village Council', ' Community Council']


class NewBrunswickMunicipalitiesPersonScraper(CanadianScraper):

    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)
        types = page.xpath('//div[@class="bluearrow shaded bottomborder "][1]/ul/li/a/@href')[:4]
        for org_type, link in enumerate(types):
            page = self.lxmlize(link)
            district_urls = page.xpath('//div[@class="parbase list section cplist"]/table/tr/td[1]/b/a/@href')
            for district_url in district_urls:
                page = self.lxmlize(district_url)
                district = page.xpath('//div[@class="pageHeader"]/h1/text()')[0].split(' - ')[1].strip()

                org = Organization(name=district + org_types[org_type], classification='legislature', jurisdiction_id=self.jurisdiction.jurisdiction_id)
                org.add_source(district_url)
                yield org

                address = ', '.join(page.xpath('//div[@class="left_contents"]/p[1]/text()'))
                contacts = page.xpath('//div[@class="left_contents"]/p[b[text() = "Contact"]]/text()')
                phone = contacts[0].split(':')[1].strip().replace(' ', '-')
                fax = contacts[1].split(':')[1].strip().replace(' ', '-')
                email = page.xpath('//div[@class="left_contents"]//a[contains(@href, "mailto:")]')
                if email:
                    email = email[0].text_content()

                site = page.xpath('//div[@class="left_contents"]//a[not(contains(@href,"mailto:"))]')
                if site:
                    site = site[0].text_content()

                councillors = page.xpath('//div[@class="right_contents"]//p/text()')
                for i, councillor in enumerate(councillors):
                    if 'Vacant' in councillor:
                        continue
                    p = Person(primary_org='legislature', name=councillor, district=district)
                    p.add_source(COUNCIL_PAGE)
                    p.add_source(link)
                    p.add_source(district_url)

                    if i == 0:
                        membership = p.add_membership(org, role='Mayor')
                    else:
                        membership = p.add_membership(org, role='Councillor')

                    membership.post_id = district
                    membership.add_contact_detail('address', address, 'legislature')
                    if phone:
                        membership.add_contact_detail('voice', phone, 'legislature')
                    if fax:
                        membership.add_contact_detail('fax', fax, 'legislature')
                    if email:
                        membership.add_contact_detail('email', email)
                    if site:
                        p.add_link(site)
                    yield p
