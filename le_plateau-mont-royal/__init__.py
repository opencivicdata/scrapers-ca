from pupa.scrape import Jurisdiction

# from .events import TorontoEventScraper
from montreal import MontrealPersonScraper
# from .votes import TorontoVoteScraper
from utils import lxmlize

import re

class Le_Plateau_Mont_Royal(Jurisdiction):
  jurisdiction_id = 'ca-qc-le_plateau-mont-royal'
  geographic_code = 2466023
  def get_metadata(self):
    return {
      'name': 'Le Plateau-Mont-Royal',
      'legislature_name': 'Le Plateau-Mont-Royal Borough Council',
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
      # '_ignored_scraped_sessions': ['2006-2010'],
    }

  def get_scraper(self, term, session, scraper_type):
    # if scraper_type == 'events':
    #     return TorontoEventScraper
    if scraper_type == 'people':
        return MontrealPersonScraper
    # if scraper_type == 'votes':
    #     return TorontoVoteScraper

  def scrape_session_list(self):
    return ['2010-2014']
    