from pupa.scrape import Jurisdiction

from .people import SaskatoonPersonScraper
from utils import lxmlize

import re

class Saskatoon(Jurisdiction):
  jurisdiction_id = 'ca-sa-saskatoon'
  geographic_code = 4711066
  def get_metadata(self):
    return {
      'name': 'Saskatoon',
      'legislature_name': 'Saskatoon City Council',
      'legislature_url': "http://www.saskatoon.ca/CITY%20COUNCIL/YOUR%20WARD%20COUNCILLORS/Pages/default.aspx",
      'terms': [{
        'name': '2010-2014',
        'sessions': ['2010-2014'],
        'start_year': 2010,
        'end_year': 2014,
      }],
      'provides': ['people'],
      'parties': [],
      'session_details': {
        '2010-2014': {
          '_scraped_name': '2010-2014',
        }
      },
      'feature_flags': [],
    }

  def get_scraper(self, term, session, scraper_type):
    if scraper_type == 'people':
        return SaskatoonPersonScraper

  def scrape_session_list(self):
    return ['2010-2014']
    