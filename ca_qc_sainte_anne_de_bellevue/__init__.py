from pupa.scrape import Jurisdiction

from .people import SainteAnneDeBellevuePersonScraper
from utils import lxmlize

class SainteAnneDeBellevue(Jurisdiction):
  jurisdiction_id = 'ocd-jurisdiction/country:ca/csd:2466117/council'
  geographic_code = 2466117
  def get_metadata(self):
    return {
      'name': 'Sainte-Anne-de-Bellevue',
      'legislature_name': 'Sainte-Anne-de-Bellevue City Council',
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
        return SainteAnneDeBellevuePersonScraper

  def scrape_session_list(self):
    return ['N/A']
    