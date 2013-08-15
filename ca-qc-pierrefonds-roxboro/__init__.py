from pupa.scrape import Jurisdiction

from montreal import MontrealPersonScraper
from utils import lxmlize

import re

class Pierrefonds_Roxboro(Jurisdiction):
  jurisdiction_id = 'ca-qc-pierrefonds-roxboro'

  def get_metadata(self):
    return {
      'name': 'Pierrefonds-Roxboro',
      'legislature_name': 'Pierrefonds-Roxboro Borough Council',
      'legislature_url': 'http://depot.ville.montreal.qc.ca/bd-elus/data.json',
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
        return MontrealPersonScraper

  def scrape_session_list(self):
    return ['2010-2014']
    