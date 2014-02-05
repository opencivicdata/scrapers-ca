from pupa.scrape import Scraper

from utils import lxmlize, CanadianLegislator as Legislator

import re

COUNCIL_PAGE = 'http://www.whitby.ca/en/townhall/meetyourcouncil.asp'


class WhitbyPersonScraper(Scraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)

    councillors = page.xpath('//table[@class=" "]/tbody//tr')[1:]
    for councillor in councillors:
      info = councillor.xpath('./td[2]/p/strong/em/text()')
      if not info:
        continue
      name, role = info[0].split(',')
      if len(info) > 1:
        role = info[1]
      role = role.strip()
      name = name.strip()
      if role == 'Councillor':
        district = councillor.xpath('./td[2]/p/strong/text()')[0].replace('Councillor', '')
      else:
        district = 'Whitby'

      email = councillor.xpath('.//a[contains(@href, "mailto:")]/@href')[0].split(':')[1]

      p = Legislator(name=name, post_id=district, role=role)
      p.add_source(COUNCIL_PAGE)
      p.add_contact('email', email, None)
      p.image = councillor.xpath('.//img/@src')[0]
      yield p
