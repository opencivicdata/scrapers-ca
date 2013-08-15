from pupa.scrape import Jurisdiction

from .people import Sainte_JeromePersonScraper
from utils import lxmlize

class Sainte_Jerome(Jurisdiction):
  jurisdiction_id = 'ocd-jurisdiction/country:ca/csd:2475017/council'
  geographic_code = 2475017
  def get_metadata(self):
    return {
      'name': 'Sainte-Jerome',
      'legislature_name': 'Sainte-Jerome City Council',
      'legislature_url': 'http://www.ville.saint-jerome.qc.ca/pages/aSavoir/conseilMunicipal.aspx',
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
        return Sainte_JeromePersonScraper

  def scrape_session_list(self):
    return ['N/A']
    