from pupa.scrape import Scraper, Legislator

from utils import lxmlize

import re

COUNCIL_PAGE = 'http://www.woolwich.ca/en/council/council.asp'


class WoolwichPersonScraper(Scraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)

    councillors = page.xpath('//div[@id="printArea"]//strong')
    for councillor in councillors:
      info = councillor.xpath('./parent::p/text()')
      if not info:
        info = councillor.xpath('./parent::div/text()')
      info = [x for x in info if x.strip()]
      district = info.pop(0)
      if 'Mayor' in district:
        district = 'Woolwich'
      else:
        district = district.replace('Councillor', '').strip()

      p = Legislator(name=councillor.text_content(), post_id=district)
      p.add_source(COUNCIL_PAGE)

      for contact in info:
        note, num = contact.split(':')
        num = num.strip().replace('(','').replace(') ', '-').replace('extension ', 'x')
        p.add_contact('phone', num, note)
      yield p