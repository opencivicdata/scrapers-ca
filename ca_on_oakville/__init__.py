from utils import CanadianJurisdiction, lxmlize

import re


class Oakville(CanadianJurisdiction):
  jurisdiction_id = u'ocd-jurisdiction/country:ca/csd:3524001/council'
  geographic_code = 3524001
  division_name = 'Oakville'
  name = 'Oakville Town Council'
  url = 'http://www.oakville.ca'
  terms = [{
    'name': '2010-2014',
    'sessions': ['2010-2014'],
    'start_year': 2010,
    'end_year': 2014,
  }]
  session_details = {
    '2010-2014': {
      '_scraped_name': '2010-2014',
    }
  }

  def scrape_session_list(self):
    page = lxmlize('http://www.oakville.ca/townhall/council.html')
    terms = page.xpath("//div[@class='colsevenfive multicol']//ul//li//a[contains(text(),'Orientation Manual')]")[0]
    terms = re.match(r'([0-9]{4})-([0-9]{4})', terms.text_content()).group()
    return [terms]
