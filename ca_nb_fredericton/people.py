from pupa.scrape import Scraper, Legislator

from utils import lxmlize

import re

COUNCIL_PAGE = 'http://www.fredericton.ca/en/citygovernment/CityCouncil.asp'


class FrederictonPersonScraper(Scraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)

    councillors = page.xpath('//table/tbody/tr/td')
    for councillor in councillors:
      text = councillor.xpath('.//strong/text()')[0]
      name = text.split(',')[0]
      if 'Deputy Mayor' in text:
        role = 'Deputy Mayor'
        district = 'Fredericton'
      elif 'Mayor' in text:
        role = 'Mayor'
        district = 'Fredericton'
      else:
        district = re.findall(r'(Ward:.*)(?=Address:)', councillor.text_content())[0].replace(':', '').strip()
        role = 'Councillor'

      p = Legislator(name=name, post_id=district, role=role)
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

      fax = re.findall(r'(?<=Fax: \().*(?=E-mail)', councillor.text_content())[0].replace(') ', '-')
      p.add_contact('fax', fax, 'legislature')

      yield p
