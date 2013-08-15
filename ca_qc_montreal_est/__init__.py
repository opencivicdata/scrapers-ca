from pupa.scrape import Jurisdiction

from .people import Montreal_EstPersonScraper
from utils import lxmlize

class Montreal_Est(Jurisdiction):
  jurisdiction_id = 'ca-qc-montreal-est'
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
        return Montreal_EstPersonScraper

  def scrape_session_list(self):
    return ['N/A']
    