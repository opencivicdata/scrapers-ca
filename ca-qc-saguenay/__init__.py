from pupa.scrape import Jurisdiction

from .people import SaguenayPersonScraper
from utils import lxmlize

import re

class Saguenay(Jurisdiction):
  jurisdiction_id = 'ca-qc-saguenay'
  geographic_code = 2494068
  def get_metadata(self):
    return {
      'name': 'Saguenay',
      'legislature_name': 'Saguenay City Council',
      'legislature_url': 'http://ville.saguenay.ca/fr/administration-municipale/conseils-municipaux-et-darrondissement/membres-des-conseils',
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
        return SaguenayPersonScraper

  def scrape_session_list(self):
    return ['2010-2014']
    