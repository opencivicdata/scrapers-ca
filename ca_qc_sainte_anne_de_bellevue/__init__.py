from pupa.scrape import Jurisdiction

from .people import Sainte_Anne_de_BellevuePersonScraper
from utils import lxmlize

class Sainte_Anne_de_Bellevue(Jurisdiction):
  jurisdiction_id = 'ocd-jurisdiction/country:ca/csd:2466117/council'
  geographic_code = 2466117
  def get_metadata(self):
    return {
      'name': 'Sainte-Anne-de-Bellevue',
      'legislature_name': 'Sainte_Anne_de_Bellevue City Council',
      'legislature_url': 'http://www.ville.sainte-anne-de-bellevue.qc.ca/Democratie.aspx',
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
        return Sainte_Anne_de_BellevuePersonScraper

  def scrape_session_list(self):
    return ['N/A']
    