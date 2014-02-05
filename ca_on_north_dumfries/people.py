from pupa.scrape import Scraper

from utils import lxmlize, CanadianLegislator as Legislator

import re

COUNCIL_PAGE = 'http://www.northdumfries.ca/en/ourtownship/MeetYourCouncil.asp'


class NorthDumfriesPersonScraper(Scraper):

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
        district = 'Ward %s' % info.pop(0).strip()
        role = 'Councillor'
      p = Legislator(name=name, post_id=district, role=role)
      p.add_source(COUNCIL_PAGE)
      p.add_contact('voice', info[0], 'legislature')
      p.add_contact('email', info[1], None)
      yield p
