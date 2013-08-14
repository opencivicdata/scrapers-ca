from pupa.scrape import Jurisdiction

# from .events import TorontoEventScraper
from .people import Grand_Prarie_No_1PersonScraper
# from .votes import TorontoVoteScraper
from utils import lxmlize

import re

class Grand_Prarie_No_1(Jurisdiction):
  jurisdiction_id = 'ca-ab-grand_prarie_no_1'
  geo_code = 4819006
  def get_metadata(self):
    return {
      'name': 'Grand_Prarie_No_1',
      'legislature_name': 'Grand_Prarie_No_1 City Council',
      'legislature_url': 'http://cms.burlington.ca/Page110.aspx',
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
        return Grand_Prarie_No_1PersonScraper
    # if scraper_type == 'votes':
    #     return TorontoVoteScraper

  def scrape_session_list(self):
    return ['2010-2014']
    