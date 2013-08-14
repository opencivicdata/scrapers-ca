from pupa.scrape import Jurisdiction

# from .events import TorontoEventScraper
from .people import SudburyPersonScraper
# from .votes import TorontoVoteScraper
from utils import lxmlize

import re

class Gatineau(Jurisdiction):
  jurisdiction_id = 'ca-qc-sudbury'
  geographic_code = 3553005
  def get_metadata(self):
    return {
      'name': 'Sudbury',
      'legislature_name': 'Sudbury City Council',
      'legislature_url': 'http://www.greatersudbury.ca/inside-city-hall/city-council/',
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
      # '_ignored_scraped_sessions': ['2006-2010'],
    }

  def get_scraper(self, term, session, scraper_type):
    # if scraper_type == 'events':
    #     return TorontoEventScraper
    if scraper_type == 'people':
        return SudburyPersonScraper
    # if scraper_type == 'votes':
    #     return TorontoVoteScraper

  def scrape_session_list(self):
    return ['2010-2014']
    