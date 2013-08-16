from pupa.scrape import Scraper, Legislator
from pupa.models import Person
from pupa.models import Organization

from utils import lxmlize

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
        district = 'dorval'
      else:
        district = info[2]
      p = Legislator(name=name, post_id=district)
      p.add_source(COUNCIL_PAGE)

      email = councillor.xpath('.//a[contains(@href, "mailto:")]/text()')[0]
      p.add_contact('email', email, None)

      yield p