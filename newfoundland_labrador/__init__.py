from pupa.scrape import Jurisdiction

from .people import Newfoundland_LabradorPersonScraper
from utils import lxmlize

import re

class Newfoundland_Labrador(Jurisdiction):
  jurisdiction_id = 'ca-nl'
  geographic_code = 10
  def get_metadata(self):
    return {
      'name': 'Newfoundland Labrador',
      'legislature_name': 'Newfoundland Labrador Municipal Council',
      'legislature_url': 'http://www.ma.gov.nl.ca/ma/municipal_directory/index.html',
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
        return Newfoundland_LabradorPersonScraper

  def scrape_session_list(self):
    return ['2010-2014']
    