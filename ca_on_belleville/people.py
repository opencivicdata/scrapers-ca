from pupa.scrape import Scraper

from utils import lxmlize, CanadianLegislator as Legislator

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

      district = councillor.xpath('./ancestor::tr/preceding-sibling::tr//font[@color="#000080"]')[0].text_content().title().replace('Councillors', '')
      role = 'Councillor'
      if not 'ward' in district:
        district = 'Belleville'
        role = 'Mayor'

      p = Legislator(name=name, post_id=district, role=role)
      p.add_source(COUNCIL_PAGE)

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
          p.add_contact('fax', number, 'legislature')
        elif 'phone' in contact_type:
          p.add_contact('voice', number, 'legislature')
        else:
          p.add_contact('voice', number, contact_type) # @todo
      yield p
