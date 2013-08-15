from pupa.scrape import Jurisdiction

from .people import FrederictonPersonScraper
from utils import lxmlize

import re

class Fredericton(Jurisdiction):
  jurisdiction_id = 'ca-nb-fredericton'
  geographic_code = 1310032
  def get_metadata(self):
    return {
      'name': 'Fredericton',
      'legislature_name': 'Fredericton City Council',
      'legislature_url': 'http://www.fredericton.ca/en/citygovernment/CityCouncil.asp',
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
        return FrederictonPersonScraper

  def scrape_session_list(self):
    return ['2010-2014']
    