from pupa.scrape import Jurisdiction

from .people import Dollard_Des_OrmeauxPersonScraper
from utils import lxmlize

class Dollard_Des_Ormeaux(Jurisdiction):
  jurisdiction_id = 'ca-qc-dollard-des-ormeaux'
  geographic_code = 2466142
  def get_metadata(self):
    return {
      'name': 'Dollard-Des-Ormeaux',
      'legislature_name': 'Dollard-Des-Ormeaux City Council',
      'legislature_url': 'http://www.ville.ddo.qc.ca/en/default.asp?contentID=17',
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
        return Dollard_Des_OrmeauxPersonScraper

  def scrape_session_list(self):
    return ['N/A']
    