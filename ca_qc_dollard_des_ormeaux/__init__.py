from pupa.scrape import Jurisdiction

from .people import DollardDesOrmeauxPersonScraper
from utils import lxmlize

class DollardDesOrmeaux(Jurisdiction):
  jurisdiction_id = 'ocd-jurisdiction/country:ca/csd:2466142/council'
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
        return DollardDesOrmeauxPersonScraper

  def scrape_session_list(self):
    return ['N/A']
    