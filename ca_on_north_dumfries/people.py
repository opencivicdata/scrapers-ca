from pupa.scrape import Scraper, Legislator

from utils import lxmlize, CanadianScraper

import re

COUNCIL_PAGE = 'http://www.northdumfries.ca/en/ourtownship/MeetYourCouncil.asp'


class NorthDumfriesPersonScraper(CanadianScraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)
    organization = self.get_organization()
    yield organization

    councillors = page.xpath('//table/tbody/tr')[1:]
    for councillor in councillors:
      info = councillor.xpath('./td//text()')
      info = [x for x in info if x.strip()]
      name = info.pop(0).replace('Councillor', '')
      if 'Mayor' in name:
        district = 'North Dumfries'
        name = name.replace('Mayor','').strip()
        role = 'mayor'
      else:
        district = info.pop(0)
        role = 'councillor'
      p = Legislator(name=name, post_id=district)
      p.add_source(COUNCIL_PAGE)
      p.add_membership(organization, role=role)
      p.add_contact('phone', info[0], 'office')
      p.add_contact('email', info[1], None)
      yield p