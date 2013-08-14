from pupa.scrape import Jurisdiction

# from .events import TorontoEventScraper
from .people import CambridgePersonScraper
# from .votes import TorontoVoteScraper
from utils import lxmlize

import re

class Cambridge(Jurisdiction):
  jurisdiction_id = 'ca-on-cambridge'
  geo_code = 3530010
  def get_metadata(self):
    return {
      'name': 'Cambridge',
      'legislature_name': 'Cambridge City Council',
      'legislature_url': 'http://www.cambridge.ca/cs_mayor/wards_councillors.php?cpid=51&sid=57',
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
        return CambridgePersonScraper
    # if scraper_type == 'votes':
    #     return TorontoVoteScraper

  def scrape_session_list(self):
    return ['2010-2014']
    