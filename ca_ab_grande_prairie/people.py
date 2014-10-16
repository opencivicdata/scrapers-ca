# coding: utf-8
from __future__ import unicode_literals
from pupa.scrape import Scraper

import re

from utils import lxmlize, CanadianPerson as Person

COUNCIL_PAGE = 'http://www.cityofgp.com/index.aspx?page=718'


class GrandePrairiePersonScraper(Scraper):

  def scrape(self):
    page = lxmlize(COUNCIL_PAGE)
    for row in page.xpath(r'//table[@class="listtable"]//tr')[1:]:
      celltext = row.xpath('./td//text()')
      last, first = celltext[0].split(', ')
      name = ' '.join((first, last))
      p = Person(name=name, district='Grande Prairie', role=celltext[1])
      p.add_source(COUNCIL_PAGE)
      p.add_contact('voice', celltext[3], 'legislature')
      p.add_contact('email',
                    row.xpath('string(./td[last()]//a/@href)').split(':')[1],
                    None)
      yield p
