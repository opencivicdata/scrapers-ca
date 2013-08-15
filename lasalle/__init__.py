from pupa.scrape import Jurisdiction

from .people import LaSallePersonScraper
from utils import lxmlize

import re

class LaSalle(Jurisdiction):
  jurisdiction_id = 'ca-qc-lasalle'
  geographic_code = 3537034
  def get_metadata(self):
    return {
      'name': 'LaSalle',
      'legislature_name': 'LaSalle City Council',
      'legislature_url': 'http://www.town.lasalle.on.ca/Council/council-council.htm',
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
        return LaSallePersonScraper

  def scrape_session_list(self):
    return ['2010-2014']
    