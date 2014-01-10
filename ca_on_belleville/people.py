from pupa.scrape import Scraper, Legislator

from utils import lxmlize, CanadianScraper

import re

COUNCIL_PAGE = 'http://www.city.belleville.on.ca/CITYHALL/MAYORANDCOUNCIL/Pages/CityCouncil.aspx'


class BellevillePersonScraper(CanadianScraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)
    organization = self.get_organization()
    yield organization

    councillors = page.xpath('//font[@color="#000000"]')
    for i, councillor in enumerate(councillors):
      name = councillor.xpath('.//*[self::b or self::strong]/text()')
      if not name:
        continue
      name = name[0]

      district = councillor.xpath('./ancestor::tr/preceding-sibling::tr//font[@color="#000080"]')[0].text_content().lower().replace('councillors', '')
      role = 'councillor'
      if not 'ward' in district:
        district = 'belleville'
        role = 'mayor'

      p = Legislator(name=name, post_id=district)
      p.add_source(COUNCIL_PAGE)
      p.add_membership(organization, role=role)

      p.image = councillor.xpath('.//parent::*//img/@src')[0]

      info = councillor.xpath('./text()')
      if len(info) < 3:
        info = info + councillors[i + 1].xpath('./text()')
      info = info[2:]

      for contact in info:
        if 'Email' in contact:
          break
        contact_type, number = contact.split(':')
        if contact_type == 'Fax':
          p.add_contact('fax', number, 'office')
        elif 'phone' in contact_type:
          p.add_contact('voice', number, 'office')
        else:
          p.add_contact('voice', number, contact_type)
      yield p
