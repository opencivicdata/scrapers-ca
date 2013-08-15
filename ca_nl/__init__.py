from pupa.scrape import Jurisdiction

from .people import Newfoundland_LabradorPersonScraper
from utils import lxmlize

class Newfoundland_Labrador(Jurisdiction):
  jurisdiction_id = 'ocd-jurisdiction/country:ca/province:nl/legislature'
  geographic_code = 10
  def get_metadata(self):
    return {
      'name': 'Newfoundland Labrador',
      'legislature_name': 'Newfoundland Labrador Municipal Council',
      'legislature_url': 'http://www.ma.gov.nl.ca/ma/municipal_directory/index.html',
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
        return Newfoundland_LabradorPersonScraper

  def scrape_session_list(self):
    return ['N/A']
    