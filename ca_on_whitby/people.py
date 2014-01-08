from pupa.scrape import Scraper, Legislator

from utils import lxmlize, CanadianScraper

import re

COUNCIL_PAGE = 'http://www.whitby.ca/en/townhall/meetyourcouncil.asp'


class WhitbyPersonScraper(CanadianScraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)
    organization = self.get_organization()
    yield organization

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
        district = 'whitby'

      email = councillor.xpath('.//a[contains(@href, "mailto:")]/@href')[0].split(':')[1]

      p = Legislator(name=name, post_id=district)
      p.add_source(COUNCIL_PAGE)
      p.add_membership(organization, role=role)
      p.add_contact('email', email, None)
      p.image = councillor.xpath('.//img/@src')[0]
      yield p
