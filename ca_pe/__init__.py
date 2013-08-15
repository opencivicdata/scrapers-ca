from pupa.scrape import Jurisdiction

from .people import PrinceEdwardIslandPersonScraper
from utils import lxmlize

class PrinceEdwardIsland(Jurisdiction):
  jurisdiction_id = 'ocd-jurisdiction/country:ca/province:pe/legislature'
  geographic_code = 11
  def get_metadata(self):
    return {
      'name': 'Prince Edward Island',
      'legislature_name': 'Prince Edward Island City Council',
      'legislature_url': 'http://www.gov.pe.ca/mapp/municipalitites.php',
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
        return PrinceEdwardIslandPersonScraper

  def scrape_session_list(self):
    return ['N/A']
    