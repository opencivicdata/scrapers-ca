from pupa.scrape import Scraper, Legislator
from pupa.models import Person
from pupa.models import Organization

from utils import lxmlize

import re

COUNCIL_PAGE = 'http://www.city.belleville.on.ca/CITYHALL/MAYORANDCOUNCIL/Pages/CityCouncil.aspx'
class BellevillePersonScraper(Scraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)

    councillors = page.xpath('//font[@color="#000000"]')
    for i, councillor in enumerate(councillors):
      name = councillor.xpath('.//*[self::b or self::strong]/text()')
      if not name:
        continue
      name = name[0]

      district = councillor.xpath('./ancestor::tr/preceding-sibling::tr//font[@color="#000080"]')[0].text_content().lower().replace('councillors','')
      if not 'ward' in district:
        district = 'belleville'

      p = Legislator(name=name, post_id=district)
      p.add_source(COUNCIL_PAGE)

      info = councillor.xpath('./text()')
      if len(info) < 3:
        info = info+councillors[i+1].xpath('./text()')
      info = info[2:]

      for contact in info:
        if 'Email' in contact:
          break
        contact_type, number = contact.split(':')
        if contact_type == 'Fax':
          p.add_contact('fax', number, None)
        elif 'phone' in contact_type:
          p.add_contact('phone', number, None)
        else:
          p.add_contact('phone', number, contact_type)
      yield p