from pupa.scrape import Scraper, Legislator

from utils import lxmlize

import re

COUNCIL_PAGE = 'http://www.beaconsfield.ca/en/your-council.html'


class BeaconsfieldPersonScraper(Scraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)

    councillors = page.xpath('//h1[@class="title"]')
    for councillor in councillors:
      if not ',' in councillor.text_content():
        continue
      name, district = councillor.text_content().split(',')
      name = name.strip()
      if 'Mayor' in district:
        p = Legislator(name=name, post_id='beaconsfield')
        p.add_source(COUNCIL_PAGE)
        phone = councillor.xpath('.//parent::div/following-sibling::div[contains(text(), "514")]/text()')[0]
        phone = phone.split(':')[1].strip().replace(' ','-')
        p.add_contact('phone', phone, None)
        yield p
        continue

      district = district.split('-')[1].strip()
      p = Legislator(name=name, post_id=district)
      p.add_source(COUNCIL_PAGE)
      phone = councillor.xpath('.//parent::div/following-sibling::p[contains(text(), "514")]/text()')
      if phone:
        phone = phone[0]
        phone = phone.split(':')[1].strip().replace(' ','-')
        p.add_contact('phone', phone, None)
      yield p