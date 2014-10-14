from __future__ import unicode_literals
from pupa.scrape import Scraper

import re

from utils import lxmlize, CanadianPerson as Person

COUNCIL_PAGE = 'http://www.newmarket.ca/en/townhall/contactinformationmayorandtowncouncil.asp'


class NewmarketPersonScraper(Scraper):

  def scrape(self):
    page = lxmlize(COUNCIL_PAGE)

    councillors = page.xpath('//div[@id="printArea"]//table//tr//td')[4:-1]
    yield self.scrape_mayor(councillors[0])
    for councillor in councillors[1:]:
      name = ' '.join(councillor.xpath('string(.//strong/a[last()])').split())
      infostr = councillor.xpath('string(.//strong)')
      try:
        district = infostr.split('-')[1]
        role = 'Councillor'
      except IndexError:
        district = 'Newmarket'
        role = 'Regional Councillor'
      url = councillor.xpath('.//a/@href')[0]

      p = Person(name=name, post_id=district, role=role)
      p.add_source(COUNCIL_PAGE)
      p.add_source(url)

      p.image = councillor.xpath('.//img/@src')[0]

      page = lxmlize(url)
      info = page.xpath('//div[@id="printArea"]')[0]
      info = info.xpath('.//p[@class="heading"][2]/following-sibling::p')
      address = info.pop(0).text_content().strip()
      if not address:
        address = info.pop(0).text_content().strip()

      if 'Ward' in info[0].text_content():
        info.pop(0)

      numbers = info.pop(0).text_content().split(':')
      email = page.xpath('//a[contains(@href, "mailto:")]/text()')[0]
      p.add_contact('email', email, None)
      for i, contact in enumerate(numbers):
        if i == 0:
          continue
        if '@' in contact:
          continue  # executive assistant email
        else:
          number = re.findall(r'([0-9]{3}-[0-9]{3}-[0-9]{4})', contact)[0]
          ext = re.findall(r'(Ext\. [0-9]{3,4})', contact)
          if ext:
            number = number + ext[0].replace('Ext. ', ' x')
          contact_type = re.findall(r'[A-Za-z]+$', numbers[i - 1])[0]
        if 'Fax' in contact_type:
          p.add_contact('fax', number, 'legislature')
        elif 'Phone' in contact_type:
          p.add_contact('voice', number, 'legislature')
        else:
          p.add_contact(contact_type, number, contact_type)
      site = page.xpath('.//a[contains(text(), "http://")]')
      if site:
        p.add_link(site[0].text_content(), None)
      yield p

  def scrape_mayor(self, div):
    name = ' '.join(div.xpath('.//strong/text()')[0].replace(',', '').split())
    p = Person(name=name, post_id='Newmarket', role='Mayor')
    p.add_source(COUNCIL_PAGE)

    numbers = div.xpath('./p/text()')
    for number in numbers:
      try:
        num_type, number = number.split(':')
        if 'Fax' in num_type:
          p.add_contact('fax', number, 'legislature')
        else:
          p.add_contact(num_type, number, num_type)
      except ValueError:
        pass
    email = div.xpath('.//a[contains(@href, "mailto:")]')[0].text_content()
    p.add_contact('email', email, None)
    return p
