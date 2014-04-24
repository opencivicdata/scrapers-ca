from __future__ import unicode_literals

from utils import CanadianJurisdiction, lxmlize

import re


class Vaughan(CanadianJurisdiction):
  jurisdiction_id = 'ocd-jurisdiction/country:ca/csd:3519028/council'
  geographic_code = 3519028
  division_name = 'Vaughan'
  name = 'Vaughan City Council'
  url = 'https://www.vaughan.ca'
  sessions = [{
    'name': '2010-2014',
    '_scraped_name': '2010-2014',
  }]

  def scrape_session_list(self):
    page = lxmlize('http://www.vaughan.ca/council/Pages/default.aspx')
    session = page.xpath('//*[@id="WebPartTitleWPQ2"]/h3/span[1]')[0].text_content()
    session = re.findall(r'[0-9]{4}-[0-9]{4}', session)[0]
    return [str(session)]
