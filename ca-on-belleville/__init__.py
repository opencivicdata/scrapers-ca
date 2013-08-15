from pupa.scrape import Jurisdiction

from .people import BellevillePersonScraper
from utils import lxmlize

import re

class Belleville(Jurisdiction):
  jurisdiction_id = 'ca-on-belleville'
  geographic_code = 3512005
  def get_metadata(self):
    return {
      'name': 'Belleville',
      'legislature_name': 'Belleville City Council',
      'legislature_url': 'http://www.city.belleville.on.ca/CITYHALL/MAYORANDCOUNCIL/Pages/CityCouncil.aspx',
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
        return BellevillePersonScraper

  def scrape_session_list(self):
    return ['2010-2014']
    