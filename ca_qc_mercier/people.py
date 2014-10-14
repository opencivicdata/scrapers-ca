from __future__ import unicode_literals
from pupa.scrape import Scraper

import re

from utils import lxmlize, CanadianPerson as Person

COUNCIL_PAGE = 'http://www.ville.mercier.qc.ca/02_viedemocratique/default.asp'


class MercierPersonScraper(Scraper):

  def scrape(self):
    page = lxmlize(COUNCIL_PAGE, user_agent='Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)')

    councillors = page.xpath('//table[@width="800"]/tr')
    for councillor in councillors:
      if councillor == councillors[0]:
        name = councillor.xpath('.//strong/text()')[0].replace('Monsieur', '').replace('Madame', '').strip()
        role = 'Maire'
      else:
        name = councillor.xpath('.//strong/text()')[0]
        name = name.replace('Monsieur', '').replace('Madame', '').strip()
        role = 'Conseiller'

      district = 'Mercier'
      email = councillor.xpath('.//a[contains(@href, "mailto:")]/@href')[0].replace('mailto:', '')

      p = Person(name=name, post_id=district, role=role)
      p.add_source(COUNCIL_PAGE)
      p.add_contact('email', email, None)
      yield p
