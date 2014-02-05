from pupa.scrape import Scraper

from utils import lxmlize, CanadianLegislator as Legislator

import re

COUNCIL_PAGE = 'http://www.milton.ca/en/townhall/mayorandcouncil.asp?_mid_=5972'


class MiltonPersonScraper(Scraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)

    councillors = page.xpath('//table[@id="Table1table"]/tbody/tr')[1:]
    for councillor in councillors:
      name = councillor.xpath('./td[2]/p/text()')[1]
      role = councillor.xpath('./td[2]/p/text()')[0].strip()
      if role == 'Local & Regional Councillor':
        role = 'Regional Councillor'
      if len(councillor.xpath('./td[2]/p/text()')) < 3:
        district = 'Milton'
      else:
        district = councillor.xpath('./td[2]/p/text()')[2]

      p = Legislator(name=name, post_id=district, role=role)
      p.add_source(COUNCIL_PAGE)

      p.image = councillor.xpath('./td[1]/p//img/@src')[0]

      if councillor == councillors[0]:
        address = ', '.join(councillor.xpath('./td[3]/p[1]/text()')).replace('Email:', '').strip()
        p.add_contact('address', address, 'legislature')

      numbers = councillor.xpath('./td[3]/p[2]/text()')
      for number in numbers:
        num_type, number = number.split(':')
        number = number.replace(', ext ', ' x').strip()
        p.add_contact(num_type, number, num_type)
      yield p
