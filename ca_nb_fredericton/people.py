from pupa.scrape import Scraper, Legislator

from utils import lxmlize

import re

COUNCIL_PAGE = 'http://www.fredericton.ca/en/citygovernment/CityCouncil.asp'


class FrederictonPersonScraper(Scraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)

    councillors = page.xpath('//table/tbody/tr/td')
    for councillor in councillors:
      name = councillor.xpath('.//strong/text()')[0].split(',')[0]
      if 'Mayor' in councillor.xpath('.//strong/text()')[0]:
        district = 'fredericton'
      else:
        district = re.findall(r'(Ward:.*)(?=Address:)', councillor.text_content())[0].replace(':', '').strip()

      p = Legislator(name=name, post_id=district)
      p.add_source(COUNCIL_PAGE)

      address = re.findall(r'(?<=Address:).*(?=Home:)', councillor.text_content())[0].strip()
      p.add_contact('address', address, None)

      phone = re.findall(r'(?<=Home: \().*(?=Fax:)', councillor.text_content())[0]
      phone = re.sub(r'(?<=[0-9])(\)\D{1,2})(?=[0-9])', '-', phone).split()[0]
      p.add_contact('phone', phone, 'Home')

      phone = re.findall(r'(?<=Office: \().*(?=Fax:)', councillor.text_content())
      if phone:
        phone = phone[0].replace(') ', '-')
        p.add_contact('phone', phone, 'office')

      fax = re.findall(r'(?<=Fax: \().*(?=E-mail)', councillor.text_content())[0].replace(') ', '-')
      p.add_contact('fax', fax, None)

      yield p
