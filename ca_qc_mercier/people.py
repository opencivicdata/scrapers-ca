from pupa.scrape import Scraper

from utils import lxmlize, CanadianLegislator as Legislator

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
        district = 'Mercier'
        role = 'Mayor'
      else:
        name, district = councillor.xpath('.//span')[0].text_content().split('Conseiller')
        name = name.replace('Monsieur', '').replace('Madame', '').strip()
        district = district.strip()
        role = 'Councillor'
      email = councillor.xpath('.//a[contains(@href, "mailto:")]/@href')[0].replace('mailto:', '')

      p = Legislator(name=name, post_id=district, role=role)
      p.add_source(COUNCIL_PAGE)
      p.add_contact('email', email, None)
      p.image = councillor.xpath('.//img/@src')[0]
      yield p
