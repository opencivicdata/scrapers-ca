from __future__ import unicode_literals
from pupa.scrape import Scraper

import re

from utils import lxmlize, CanadianPerson as Person

COUNCIL_PAGE = 'http://www.fredericton.ca/en/citygovernment/CityCouncil.asp'


class FrederictonPersonScraper(Scraper):

  def scrape(self):
    page = lxmlize(COUNCIL_PAGE)

    councillors = page.xpath('//table/tbody/tr/td')
    for councillor in councillors:
      text = councillor.xpath('.//strong/text()')[0]
      name = text.split(',')[0].replace('Name:', '').strip()
      if 'Mayor' in text and not 'Deputy Mayor' in text:
        role = 'Mayor'
        district = 'Fredericton'
      else:
        district = re.findall(r'(Ward:.*)(?=Address:)', councillor.text_content())[0].replace(':', '').strip()
        district = re.search('\((.+?)(?: Area)?\)', district).group(1)
        role = 'Councillor'

      p = Person(name=name, district=district, role=role)
      p.add_source(COUNCIL_PAGE)

      p.image = councillor.xpath('.//img/@src')[0]

      address = re.findall(r'(?<=Address:).*(?=Home:)', councillor.text_content())[0].strip()
      p.add_contact('address', address, 'legislature')

      phone = re.findall(r'(?<=Home: \().*(?=Fax:)', councillor.text_content())[0]
      phone = re.sub(r'(?<=[0-9])(\)\D{1,2})(?=[0-9])', '-', phone).split()[0]
      p.add_contact('voice', phone, 'residence')

      phone = re.findall(r'(?<=Office: \().*(?=Fax:)', councillor.text_content())
      if phone:
        phone = phone[0].replace(') ', '-')
        p.add_contact('voice', phone, 'legislature')

      yield p
