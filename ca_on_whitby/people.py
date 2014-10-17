from __future__ import unicode_literals
from pupa.scrape import Scraper

import re

from utils import CanadianScraper, CanadianPerson as Person

COUNCIL_PAGE = 'http://www.whitby.ca/en/townhall/meetyourcouncil.asp'


class WhitbyPersonScraper(CanadianScraper):

  def scrape(self):
    page = self.lxmlize(COUNCIL_PAGE)

    person_elems = page.xpath('//tr')
    for person in person_elems:
      info = person[1]
      try:  # Mayor and regional councillors
        name, role = info[0].text_content().split(',')
        role = role.strip()
        district = 'Whitby'
      except ValueError:
        district = ' '.join(info[0].text_content().split()[:2])
        name, role = info[1].text_content().split(', ')
      email = info.xpath('string(.//a/@href)')[len('mailto:'):].split(';')[0]
      image = person.xpath('string(.//img/@src)')
      p = Person(primary_org='legislature', name=name, district=district, role=role, image=image)
      p.add_source(COUNCIL_PAGE)
      p.add_contact('email', email)
      yield p
