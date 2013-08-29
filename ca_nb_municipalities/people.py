from pupa.scrape import Scraper, Legislator
from pupa.models import Organization

from utils import lxmlize

import re

COUNCIL_PAGE = 'http://www2.gnb.ca/content/gnb/en/departments/elg/local_government/content/community_profiles.html'
org_types = [' city council', ' town council', ' village council', ' community council']


class NewBrunswickPersonScraper(Scraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)
    types = page.xpath('//div[@class="bluearrow shaded bottomborder "][1]/ul/li/a/@href')[:4]
    for org_type, link in enumerate(types):
      page = lxmlize(link)
      district_urls = page.xpath('//div[@class="parbase list section cplist"]/table/tr/td[1]/b/a/@href')
      for district_url in district_urls:
        page = lxmlize(district_url)
        district = page.xpath('//div[@class="pageHeader"]/h1/text()')[0].split('-')[1].strip()

        org_name = district + org_types[org_type]
        org = Organization(name=org_name, classification='legislature', jurisdiction_id=self.jurisdiction.jurisdiction_id)
        org.add_source(district_url)
        yield org

        address = ', '.join(page.xpath('//div[@class="left_contents"]/p[1]/text()'))
        contacts = page.xpath('//div[@class="left_contents"]/p[3]/text()')
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
          p = Legislator(name=councillor, post_id=district)
          p.add_source(COUNCIL_PAGE)
          p.add_source(link)
          p.add_source(district_url)

          if i == 0:
            p.add_membership(org, role='mayor')
          else:
            p.add_membership(org, role='councillor')

          p.add_contact('address', address, 'office')
          if phone:
            p.add_contact('phone', phone, 'office')
          if fax:
            p.add_contact('fax', fax, 'office')
          if email:
            p.add_contact('email', email, None)
          if site:
            p.add_link(site, 'district site')
          yield p
