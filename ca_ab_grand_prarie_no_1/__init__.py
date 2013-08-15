from pupa.scrape import Jurisdiction

from .people import Grand_Prarie_No_1PersonScraper
from utils import lxmlize

class Grand_Prarie_No_1(Jurisdiction):
  jurisdiction_id = 'ca-ab-grand_prarie_no_1'
  geographic_code = 4819006
  def get_metadata(self):
    return {
      'name': 'Grand_Prarie_No_1',
      'legislature_name': 'Grand_Prarie_No_1 City Council',
      'legislature_url': 'http://cms.burlington.ca/Page110.aspx',
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
        return Grand_Prarie_No_1PersonScraper

  def scrape_session_list(self):
    return ['N/A']
    