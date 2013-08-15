from pupa.scrape import Jurisdiction

from .people import SennevillePersonScraper
from utils import lxmlize

import re

class Senneville(Jurisdiction):
  jurisdiction_id = 'ca-qc-senneville'
  geographic_code = 2466127
  def get_metadata(self):
    return {
      'name': 'Senneville',
      'legislature_name': 'Senneville City Council',
      'legislature_url': 'http://www.villagesenneville.qc.ca/fr/membres-du-conseil-municipal',
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
        return SennevillePersonScraper

  def scrape_session_list(self):
    return ['2010-2014']
    