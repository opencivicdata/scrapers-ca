from pupa.scrape import Jurisdiction

from .people import Chatham_KentPersonScraper
from utils import lxmlize

import re

class Chatham_Kent(Jurisdiction):
  jurisdiction_id = 'ca-on-chatham-kent'
  geographic_code = 3536020
  def get_metadata(self):
    return {
      'name': 'Chatham-Kent',
      'legislature_name': 'Chatham-Kent City Council',
      'legislature_url': 'http://www.chatham-kent.ca/Council/councilmembers/Pages/CouncilMembers.aspx',
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
        return Chatham_KentPersonScraper

  def scrape_session_list(self):
    return ['2010-2014']
    