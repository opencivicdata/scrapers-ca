from pupa.scrape import Jurisdiction

# from .events import TorontoEventScraper
from .people import Dollard_Des_OrmeauxPersonScraper
# from .votes import TorontoVoteScraper
from .utils import lxmlize

import re

class Dollard_Des_Ormeaux(Jurisdiction):
  jurisdiction_id = 'ca-qc-dollard-des-ormeaux'

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
      # '_ignored_scraped_sessions': ['2006-2010'],
    }

  def get_scraper(self, term, session, scraper_type):
    # if scraper_type == 'events':
    #     return TorontoEventScraper
    if scraper_type == 'people':
        return Dollard_Des_OrmeauxPersonScraper
    # if scraper_type == 'votes':
    #     return TorontoVoteScraper

  def scrape_session_list(self):
    return ['2010-2014']
    