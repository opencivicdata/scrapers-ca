from pupa.scrape import Jurisdiction

from .people import MontrealEstPersonScraper
from utils import lxmlize

class MontrealEst(Jurisdiction):
  jurisdiction_id = 'ocd-jurisdiction/country:ca/csd:2466007/council'
  geographic_code = 2466007
  def get_metadata(self):
    return {
      'name': 'Montreal-Est',
      'legislature_name': 'Montreal-Est City Council',
      'legislature_url': 'http://ville.montreal-est.qc.ca/site2/index.php?option=com_content&view=article&id=12&Itemid=59',
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
        return MontrealEstPersonScraper

  def scrape_session_list(self):
    return ['N/A']
    