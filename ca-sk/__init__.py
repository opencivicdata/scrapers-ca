from pupa.scrape import Jurisdiction

from .people import SaskatchewanPersonScraper
from utils import lxmlize

import re

class Saskatchewan(Jurisdiction):
  jurisdiction_id = 'ca-sk'
  geographic_code = 47
  def get_metadata(self):
    return {
      'name': 'Saskatchewan',
      'legislature_name': 'Saskatchewan City Council',
      'legislature_url': 'http://www.municipal.gov.sk.ca/Programs-Services/Municipal-Directory-pdf',
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
        return SaskatchewanPersonScraper

  def scrape_session_list(self):
    return ['2010-2014']
    