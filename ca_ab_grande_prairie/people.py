# coding: utf-8
from pupa.scrape import Scraper

from utils import lxmlize, CanadianLegislator as Legislator

import re

COUNCIL_PAGE = 'http://www.cityofgp.com/index.aspx?page=718'


class GrandePrairiePersonScraper(Scraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)
    for row in page.xpath(r'//table[@class="listtable"]//tr')[1:]:
      celltext = row.xpath('./td//text()')
      last, first = celltext[0].split(', ')
      name = ' '.join((first, last))
      p = Legislator(name=name, post_id=None, role=celltext[1])
      p.add_source(COUNCIL_PAGE)
      p.post_id = 'Grande Prairie'
      p.add_contact('voice', celltext[3], 'legislature')
      p.add_contact('email', 
                    row.xpath('string(./td[last()]//a/@href)').split(':')[1],
                    None)
      yield p
