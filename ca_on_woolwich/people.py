from pupa.scrape import Scraper, Legislator

from utils import lxmlize, CanadianScraper

import re

COUNCIL_PAGE = 'http://www.woolwich.ca/en/council/council.asp'


class WoolwichPersonScraper(CanadianScraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)
    organization = self.get_organization()
    yield organization

    councillors = page.xpath('//div[@id="printArea"]//strong')
    for councillor in councillors:
      info = councillor.xpath('./parent::p/text()')
      if not info:
        info = councillor.xpath('./parent::div/text()')
      info = [x for x in info if x.strip()]
      district = info.pop(0)
      if 'Mayor' in district:
        district = 'Woolwich'
        role = 'mayor'
      else:
        district = district.replace('Councillor', '').strip()
        role = 'councillor'

      p = Legislator(name=councillor.text_content(), post_id=district)
      p.add_source(COUNCIL_PAGE)
      p.add_membership(organization, role=role)
      p.image = councillor.xpath('./img/@src')[0]

      for contact in info:
        note, num = contact.split(':')
        num = num.strip().replace('(', '').replace(') ', '-').replace('extension ', 'x')
        p.add_contact('voice', num, note)
      yield p
