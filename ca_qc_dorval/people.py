from pupa.scrape import Scraper

from utils import lxmlize, CanadianLegislator as Legislator

import re

COUNCIL_PAGE = 'http://www.ville.dorval.qc.ca/en/default.asp?contentID=516'


class DorvalPersonScraper(Scraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)

    councillors = page.xpath('//p[@align="center"]')
    for councillor in councillors:
      info = councillor.xpath('.//strong/text()')
      name = info[0]
      if len(info) < 3:
        district = 'Dorval'
        role = 'Mayor'
      else:
        district = info[2]
        role = 'Councillor'
      p = Legislator(name=name, post_id=district, role=role)
      p.add_source(COUNCIL_PAGE)

      p.image = councillor.xpath('./parent::td/parent::tr/preceding-sibling::tr//img/@src')[0]

      email = councillor.xpath('.//a[contains(@href, "mailto:")]/text()')[0]
      p.add_contact('email', email, None)

      yield p
