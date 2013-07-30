from pupa.scrape import Scraper, Legislator
from larvae.person import Person
from larvae.organization import Organization

from .utils import lxmlize

import re

COUNCIL_PAGE = 'http://www.brantford.ca/govt/council/members/Pages/default.aspx'

class BrantfordPersonScraper(Scraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)

    councillors = page.xpath('//div[@id="centre_content"]//tr')
    for councillor in councillors:
      if 'Position' in councillor.text_content():
        continue

      district = councillor.xpath('./td')[0].text_content().replace('Councillor','')
      name = councillor.xpath('./td')[1].text_content()
      url = councillor.xpath('./td/a')[0].attrib['href']

      p = Legislator(name=name, district=district)
      p.add_source(COUNCIL_PAGE)
      p.add_source(url)

      page = lxmlize(url)
      
      address = page.xpath('//div[@id="centre_content"]//p')[0].text_content()
      email = page.xpath('//a[contains(@href,"mailto:")]')[0].attrib['href'].replace('mailto:','')
      p.add_contact('address', address, None)
      p.add_contact('email', email, None)

      numbers = page.xpath('//div[@id="centre_content"]//p[contains(text(),"-")]')[0].text_content()
      if 'tel' in numbers:
        phone = re.findall(r'(.*)tel', numbers)[0].strip().replace(' ','-')
        p.add_contact('phone', phone, None)
      if 'cell' in numbers:
        cell = re.findall(r'(.*)cell', numbers)[0].strip().replace(' ','-')
        p.add_contact('phone', cell, 'cell')
      if 'fax' in numbers:
        fax = re.findall(r'(.*)fax', numbers)[0].strip().replace(' ','-')
        p.add_contact('fax', fax, None)

      if len(page.xpath('//div[@id="centre_content"]//a')) > 2:
        site = page.xpath('//div[@id="centre_content"]//a')[-1].attrib['href']
        p.add_link(site, 'personal site')
      yield p
