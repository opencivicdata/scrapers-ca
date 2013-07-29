from pupa.scrape import Jurisdiction

# from .events import TorontoEventScraper
from .people import GatineauPersonScraper
# from .votes import TorontoVoteScraper
from .utils import lxmlize

import re

class Gatineau(Jurisdiction):
  jurisdiction_id = 'ca-qc-gatineau'

  def get_metadata(self):
    return {
      'name': 'Gatineau',
      'legislature_name': 'Gatineau Municipal Council',
      'legislature_url': 'http://www.gatineau.ca/page.asp?p=la_ville/conseil_municipal',
      'terms': [{
        'name': '2009-2013',
        'sessions': ['2009-2013'],
        'start_year': 2009,
        'end_year': 2013,
      }],
      'provides': ['people'],
      'parties': [],
      'session_details': {
        '2009-2013': {
          '_scraped_name': '2009-2013',
        }
      },
      'feature_flags': [],
      # '_ignored_scraped_sessions': ['2006-2010'],
    }

  def get_scraper(self, term, session, scraper_type):
    # if scraper_type == 'events':
    #     return TorontoEventScraper
    if scraper_type == 'people':
        return GatineauPersonScraper
    # if scraper_type == 'votes':
    #     return TorontoVoteScraper

  def scrape_session_list(self):
    return ['2009-2013']
    