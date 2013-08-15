from pupa.scrape import Jurisdiction

from .people import Pointe_ClairePersonScraper
from utils import lxmlize

import re

class Pointe_Claire(Jurisdiction):
  jurisdiction_id = 'ca-qc-pointe-claire'
  geographic_code = 2466097
  def get_metadata(self):
    return {
      'name': 'Pointe-Claire',
      'legislature_name': 'Pointe-Claire City Council',
      'legislature_url': 'http://www.ville.pointe-claire.qc.ca/en/city-hall-administration/your-council/municipal-council.html',
      'terms': [{
        'name': 'N/A',
        'sessions': ['N/A'],
      }],
      'provides': ['people'],
      'session_details': {
        'N/A': {
          '_scraped_name': 'N/A',
        }
      },
    }

  def get_scraper(self, term, session, scraper_type):
    if scraper_type == 'people':
        return Pointe_ClairePersonScraper

  def scrape_session_list(self):
    return ['N/A']
    