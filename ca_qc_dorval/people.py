from __future__ import unicode_literals
from pupa.scrape import Scraper

import re

from utils import lxmlize, CanadianPerson as Person

COUNCIL_PAGE = 'http://www.ville.dorval.qc.ca/en/democratic-life/municipal-council'


class DorvalPersonScraper(Scraper):

  def scrape(self):
    page = lxmlize(COUNCIL_PAGE)

    councillors = page.xpath('//td/p[./strong]')
    for councillor in councillors:
      info = councillor.xpath('./strong/text()')
      name = info[0]
      if len(info) < 3:
        district = 'Dorval'
        role = 'Maire'
      else:
        district = info[2]
        role = 'Conseiller'
      p = Person(name=name, district=district, role=role)
      p.add_source(COUNCIL_PAGE)

      p.image = councillor.xpath('./preceding-sibling::p/img/@src')[0]

      email = councillor.xpath('.//a[contains(@href, "mailto:")]/text()')[0]
      p.add_contact('email', email, None)

      yield p
