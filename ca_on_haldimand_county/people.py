from __future__ import unicode_literals
from pupa.scrape import Scraper

import re

from utils import CanadianScraper, CanadianPerson as Person

COUNCIL_PAGE = 'http://www.haldimandcounty.on.ca/OurCounty.aspx?id=338'


class HaldimandCountyPersonScraper(CanadianScraper):

  def scrape(self):
    page = self.lxmlize(COUNCIL_PAGE)

    councillors = page.xpath('//div[@id="ctl00_ContentPlaceHolder1_ContentBlock1"]//a/parent::p')
    for councillor in councillors:
      if not councillor.text_content().strip():
        continue
      if 'Mayor' in councillor.text_content():
        name = councillor.text_content().replace('Mayor ', '')
        district = 'Haldimand County'
        role = 'Mayor'
      else:
        district, name = councillor.text_content().split(' - ')
        name = name.replace('Councillor', '').strip()
        district = district.strip()
        role = 'Councillor'

      url = councillor.xpath('.//a')[0].attrib['href']
      page = self.lxmlize(url)

      p = Person(primary_org='legislature', name=name, district=district, role=role)
      p.add_source(COUNCIL_PAGE)
      p.add_source(url)

      p.image = page.xpath('//div[@id="ctl00_ContentPlaceHolder1_ContentBlock1"]//tr[1]/td//img/@src')[0]

      info = page.xpath('//a[contains(@href, "mailto:")]/parent::*/text()')
      for i, field, in enumerate(info):
        if re.match(r'[0-9]+ [A-Z]', field):
          address = field + ', ' + info[i + 1] + ', ' + info[i + 2]
          p.add_contact('address', address, 'legislature')
        if re.findall(r'[0-9]{3} [0-9]{3} [0-9]{4}', field):
          if 'Fax' in field:
            num = field.replace('Fax: ', '').strip().replace(' ', '-')
            p.add_contact('fax', num, 'legislature')
          else:
            num = field.replace('Telephone: ', '').strip().replace(' ', '-')
            p.add_contact('voice', num, 'legislature')
      email = page.xpath('//a[contains(@href, "mailto:")]/text()')[0]
      p.add_contact('email', email)
      yield p
