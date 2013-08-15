from pupa.scrape import Jurisdiction

from .people import Prince_Edward_IslandPersonScraper
from utils import lxmlize

import re

class Prince_Edward_Island(Jurisdiction):
  jurisdiction_id = 'ca-pe'
  geographic_code = 11
  def get_metadata(self):
    return {
      'name': 'Prince Edward Island',
      'legislature_name': 'Prince Edward Island City Council',
      'legislature_url': 'http://www.gov.pe.ca/mapp/municipalitites.php',
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
        return Prince_Edward_IslandPersonScraper

  def scrape_session_list(self):
    return ['2010-2014']
    