from pupa.scrape import Jurisdiction

from .people import Dollard_Des_OrmeauxPersonScraper
from utils import lxmlize

import re

class Dollard_Des_Ormeaux(Jurisdiction):
  jurisdiction_id = 'ca-qc-dollard-des-ormeaux'
  geographic_code = 2466142
  def get_metadata(self):
    return {
      'name': 'Dollard-Des-Ormeaux',
      'legislature_name': 'Dollard-Des-Ormeaux City Council',
      'legislature_url': 'http://www.ville.ddo.qc.ca/en/default.asp?contentID=17',
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
        return Dollard_Des_OrmeauxPersonScraper

  def scrape_session_list(self):
    return ['2010-2014']
    