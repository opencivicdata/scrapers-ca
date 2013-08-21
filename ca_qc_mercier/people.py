from pupa.scrape import Scraper, Legislator

from utils import lxmlize

import re

COUNCIL_PAGE = 'http://www.ville.mercier.qc.ca/02_viedemocratique/default.asp'


class MercierPersonScraper(Scraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)

    councillors = page.xpath('//table//tr[2]//table//td')
    for councillor in councillors:
      if not councillor.text_content().strip():
        continue

      if councillor == councillors[6]:
        name = councillor.xpath('.//span')[0].text_content().replace('Maire', '').strip()
        district = 'mercier'
      else:
        name, district = councillor.xpath('.//span')[0].text_content().split('Conseiller')
        name = name.replace('Monsieur', '').replace('Madame', '').strip()
        district.strip()
      email = councillor.xpath('.//a[contains(@href, "mailto:")]/@href')[0].replace('mailto:', '')

      p = Legislator(name=name, post_id=district)
      p.add_source(COUNCIL_PAGE)
      p.add_contact('email', email, None)
      yield p
