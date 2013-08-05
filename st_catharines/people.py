from pupa.scrape import Scraper, Legislator
from larvae.person import Person
from larvae.organization import Organization

from .utils import lxmlize

import re

COUNCIL_PAGE = 'http://www.stcatharines.ca/en/governin/BrianMcMullanMayor.asp'

class St_CatharinesPersonScraper(Scraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)

    councillors = page.xpath('//li[@class="withChildren"]/ul/li/a')[1:]
    for councillor in councillors:
      page = lxmlize(councillor.attrib['href'])

      name = councillor.text_content().split(',')[0]
      district = page.xpath('//p[contains(text(), "Ward")]/text()')[0]
      if 'Mayor' in district:
        print '================================='
        district = 'St. Catharines'

      p = Legislator(name=name, district=district)
      p.add_source(COUNCIL_PAGE)
      p.add_source(councillor.attrib['href'])

      contacts = page.xpath('//div[@class="contactDetails"]')[0]
      address = contacts.xpath('.//p')[2].text_content()
      phone = contacts.xpath('.//p')[3].text_content()
      fax = contacts.xpath('.//p')[4].text_content()
      if 'Councillor' in address:
        address = contacts.xpath('.//p')[3].text_content()
        phone = contacts.xpath('.//p')[4].text_content()
        fax = contacts.xpath('.//p')[5].text_content()

      address = re.sub(r'([a-z\.])([A-Z])', r'\1, \2', address)
      phone = phone.replace('Tel: ','').replace('.','-')
      fax = fax.replace('Fax: ','').replace('.','-')
      email = contacts.xpath('.//a[contains(@href, "mailto:")]/@href')[0].replace('mailto:', '')

      p.add_contact('address', address, None)
      p.add_contact('phone', phone, None)
      p.add_contact('fax', fax, None)
      p.add_contact('email', email, None)
      yield p