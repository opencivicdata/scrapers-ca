from pupa.scrape import Jurisdiction

from montreal import MontrealPersonScraper
from utils import lxmlize

import re

class Villeray_Saint_Michel_Parc_Extension(Jurisdiction):
  jurisdiction_id = 'ca-qc-villeray-saint-michel-parc-extension'

  def get_metadata(self):
    return {
      'name': 'Villeray-Saint-Michel-Parc-Extension',
      'legislature_name': 'Villeray-Saint-Michel-Parc-Extension Borough Council',
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
    