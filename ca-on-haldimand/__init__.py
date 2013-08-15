from pupa.scrape import Jurisdiction

from .people import HaldimandPersonScraper
from utils import lxmlize

class Haldimand(Jurisdiction):
  jurisdiction_id = 'ca-on-haldimand'
  geographic_code = 3528018
  def get_metadata(self):
    return {
      'name': 'Haldimand',
      'legislature_name': 'Haldimand City Council',
      'legislature_url': 'http://www.haldimandcounty.on.ca/OurCounty.aspx?id=338',
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
        return HaldimandPersonScraper

  def scrape_session_list(self):
    return ['N/A']
    