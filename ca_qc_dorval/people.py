from pupa.scrape import Scraper, Legislator

from utils import lxmlize, CanadianScraper

import re

COUNCIL_PAGE = 'http://www.ville.dorval.qc.ca/en/default.asp?contentID=516'


class DorvalPersonScraper(CanadianScraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)
    organization = self.get_organization()
    yield organization

    councillors = page.xpath('//p[@align="center"]')
    for councillor in councillors:
      info = councillor.xpath('.//strong/text()')
      name = info[0]
      if len(info) < 3:
        district = 'dorval'
        role = 'mayor'
      else:
        district = info[2]
        role = 'councillor'
      p = Legislator(name=name, post_id=district)
      p.add_source(COUNCIL_PAGE)
      p.add_membership(organization, role=role)

      p.image = councillor.xpath('./parent::td/parent::tr/preceding-sibling::tr//img/@src')[0]

      email = councillor.xpath('.//a[contains(@href, "mailto:")]/text()')[0]
      p.add_contact('email', email, None)

      yield p
