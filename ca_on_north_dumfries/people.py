from pupa.scrape import Scraper, Legislator

from utils import lxmlize, CanadianScraper

import re

COUNCIL_PAGE = 'http://www.northdumfries.ca/en/ourtownship/MeetYourCouncil.asp'


class NorthDumfriesPersonScraper(CanadianScraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)

    councillors = page.xpath('//table/tbody/tr')[1:]
    for councillor in councillors:
      info = councillor.xpath('./td//text()')
      info = [x for x in info if x.strip()]
      name = info.pop(0).replace('Councillor', '')
      if 'Mayor' in name:
        district = 'North Dumfries'
        name = name.replace('Mayor', '').strip()
        role = 'Mayor'
      else:
        district = info.pop(0)
        role = 'Councillor'
      p = Legislator(name=name, post_id=district)
      p.add_source(COUNCIL_PAGE)
      p.role = role
      p.add_contact('voice', info[0], 'legislature')
      p.add_contact('email', info[1], None)
      yield p
