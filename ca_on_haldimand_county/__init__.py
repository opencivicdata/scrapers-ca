from pupa.scrape import Jurisdiction

from .people import HaldimandCountyPersonScraper
from utils import lxmlize

class HaldimandCounty(Jurisdiction):
  jurisdiction_id = 'ocd-jurisdiction/country:ca/csd:3528018/council'
  geographic_code = 3528018
  def get_metadata(self):
    return {
      'name': 'Haldimand County',
      'legislature_name': 'Haldimand County Council',
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
        return HaldimandCountyCountyPersonScraper

  def scrape_session_list(self):
    return ['N/A']
    