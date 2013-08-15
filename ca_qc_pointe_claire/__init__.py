from pupa.scrape import Jurisdiction

from .people import PointeClairePersonScraper
from utils import lxmlize

import re

class PointeClaire(Jurisdiction):
  jurisdiction_id = 'ocd-jurisdiction/country:ca/csd:2466097/council'
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
        return PointeClairePersonScraper

  def scrape_session_list(self):
    return ['N/A']
    