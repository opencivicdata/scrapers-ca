from pupa.scrape import Scraper, Legislator

from utils import lxmlize, CanadianScraper

import re

COUNCIL_PAGE = 'http://www.haldimandcounty.on.ca/OurCounty.aspx?id=338'


class HaldimandCountyPersonScraper(CanadianScraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)
    organization = self.get_organization()
    yield organization

    councillors = page.xpath('//div[@id="ctl00_ContentPlaceHolder1_ContentBlock1"]//a/parent::p')
    for councillor in councillors:
      if not councillor.text_content().strip():
        continue
      if 'Mayor' in councillor.text_content():
        name = councillor.text_content().replace('Mayor ', '')
        district = 'haldimand'
        role = 'mayor'
      else:
        district, name = councillor.text_content().split(' - ')
        name = name.replace('Councillor', '').strip()
        district = district.strip()
        role = 'councillor'

      url = councillor.xpath('.//a')[0].attrib['href']
      page = lxmlize(url)

      p = Legislator(name=name, post_id=district)
      p.add_source(COUNCIL_PAGE)
      p.add_source(url)
      p.add_membership(organization, role=role)

      p.image = page.xpath('//div[@id="ctl00_ContentPlaceHolder1_ContentBlock1"]//tr[1]/td/img/@src')[0]

      info = page.xpath('//a[contains(@href, "mailto:")]/parent::*/text()')
      for i, field, in enumerate(info):
        if re.match(r'[0-9]+ [A-Z]', field):
          address = field + ', ' + info[i + 1] + ', ' + info[i + 2]
          p.add_contact('address', address, 'office')
        if re.findall(r'[0-9]{3} [0-9]{3} [0-9]{4}', field):
          if 'Fax' in field:
            num = field.replace('Fax: ', '').strip().replace(' ', '-')
            p.add_contact('fax', num, 'office')
          else:
            num = field.replace('Telephone: ', '').strip().replace(' ', '-')
            p.add_contact('phone', num, 'office')
      email = page.xpath('//a[contains(@href, "mailto:")]/text()')[0]
      p.add_contact('email', email, None)
      yield p
