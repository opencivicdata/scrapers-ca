from pupa.scrape import Scraper, Legislator

from utils import lxmlize

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
        name = name.replace('Mayor','').strip()
      else:
        district = info.pop(0)

      p = Legislator(name=name, post_id=district)
      p.add_source(COUNCIL_PAGE)
      p.add_contact('phone', info[0], None)
      p.add_contact('email', info[1], None)
      yield p