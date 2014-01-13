from pupa.scrape import Scraper, Legislator

from utils import lxmlize, CanadianScraper

import re

COUNCIL_PAGE = 'http://www.fredericton.ca/en/citygovernment/CityCouncil.asp'


class FrederictonPersonScraper(CanadianScraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)

    councillors = page.xpath('//table/tbody/tr/td')
    for councillor in councillors:
      name = councillor.xpath('.//strong/text()')[0].split(',')[0]
      if 'Mayor' in councillor.xpath('.//strong/text()')[0]:
        role = 'Mayor'
        district = 'fredericton'
      else:
        district = re.findall(r'(Ward:.*)(?=Address:)', councillor.text_content())[0].replace(':', '').strip()
        role = 'Councillor'

      p = Legislator(name=name, post_id=district)
      p.add_source(COUNCIL_PAGE)
      p.role = role

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

      fax = re.findall(r'(?<=Fax: \().*(?=E-mail)', councillor.text_content())[0].replace(') ', '-')
      p.add_contact('fax', fax, 'legislature')

      yield p
