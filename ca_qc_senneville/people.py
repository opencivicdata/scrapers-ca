from pupa.scrape import Scraper, Legislator
from pupa.models import Person
from pupa.models import Organization

from utils import lxmlize

import re

COUNCIL_PAGE = 'http://www.villagesenneville.qc.ca/fr/membres-du-conseil-municipal'

class SennevillePersonScraper(Scraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)

    councillors = page.xpath('//div[@class="field-item even"]//tr')
    for councillor in councillors:
      district = councillor.xpath('./td[1]//strong/text()')[0]
      if 'Maire' in district:
        district = 'senneville'
      name = councillor.xpath('./td[2]//strong/text()')[0].lower()
      email = councillor.xpath('.//a/text()')[0]
      p = Legislator(name=name, post_id=district)
      p.add_source(COUNCIL_PAGE)
      p.add_contact('email', email, None)
      yield p