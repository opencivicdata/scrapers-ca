from __future__ import unicode_literals

from utils import CanadianJurisdiction, lxmlize

import re


class Oakville(CanadianJurisdiction):
  jurisdiction_id = 'ocd-jurisdiction/country:ca/csd:3524001/council'
  geographic_code = 3524001
  division_name = 'Oakville'
  name = 'Oakville Town Council'
  url = 'http://www.oakville.ca'
  sessions = [{
    'name': '2010-2014',
    '_scraped_name': '2010-2014',
  }]

  def scrape_session_list(self):
    page = lxmlize('http://www.oakville.ca/townhall/council.html')
    sessions = page.xpath("//div[@class='colsevenfive multicol']//ul//li//a[contains(text(),'Orientation Manual')]")[0]
    sessions = re.match(r'([0-9]{4})-([0-9]{4})', sessions.text_content()).group()
    return [sessions]
