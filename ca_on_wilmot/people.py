from __future__ import unicode_literals
from pupa.scrape import Scraper

import re

from utils import CanadianScraper, CanadianPerson as Person

COUNCIL_PAGE = 'http://www.wilmot.ca/current-council.php'


class WilmotPersonScraper(CanadianScraper):

  def scrape(self):
    page = self.lxmlize(COUNCIL_PAGE)

    councillors = page.xpath('//table[@id="Main Content"]//td[@colspan="3"]//td/p/b')
    for councillor in councillors:
      district, name = councillor.xpath('./text()')[0].split(':')
      if 'Mayor' in district:
        yield scrape_mayor(councillor, name)
        continue

      p = Person(primary_org='legislature', name=name, district=district, role='Councillor')
      p.add_source(COUNCIL_PAGE)

      base_info = councillor.xpath('./parent::p/text()')
      for info in councillor.xpath('./parent::p/following-sibling::p'):
        if info.xpath('.//b'):
          break
        base_info = base_info + info.xpath('./text()')

      address = ''
      complete = False
      while not complete:
        address = address + ' ' + base_info.pop(0)
        if re.search(r'[A-Z][0-9A-Z][A-Z] \d[A-Z]\d', address):
          complete = True
      p.add_contact('address', address, 'legislature')

      base_info.pop(-1)
      base_info = ' '.join(base_info).split()
      for i, contact in enumerate(base_info):
        if re.match(r'[0-9]', contact):
          continue
        if 'fax' in contact:
          p.add_contact('fax', base_info[i + 1], 'legislature')
        else:
          p.add_contact(contact, base_info[i + 1], contact)
      email = councillor.xpath('./parent::p/following-sibling::p/a[contains(@href, "mailto")]/text()')[0]
      p.add_contact('email', email)
      yield p


def scrape_mayor(div, name):

  p = Person(primary_org='legislature', name=name, district='Wilmot', role='Mayor')
  p.add_source(COUNCIL_PAGE)

  info = div.xpath('./parent::p//text()')
  info.pop(0)
  address = ' '.join(info[:3])
  phone = info[3].split()[1]
  fax = info[4].split()[1]
  email = info[-1]
  p.add_contact('address', address, 'legislature')
  p.add_contact('voice', phone, 'legislature')
  p.add_contact('fax', fax, 'legislature')
  p.add_contact('email', email)
  return p
