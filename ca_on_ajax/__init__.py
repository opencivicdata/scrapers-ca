from pupa.scrape import Jurisdiction

from .people import AjaxPersonScraper
from utils import lxmlize

class Ajax(Jurisdiction):
  jurisdiction_id = 'ocd-jurisdiction/country:ca/csd:3518005/council'
  geographic_code = 3518005
  def get_metadata(self):
    return {
      'name': 'Ajax',
      'legislature_name': 'Ajax City Council',
      'legislature_url': 'http://www.ajax.ca/en/insidetownhall/mayorcouncillors.asp',
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
        return AjaxPersonScraper

  def scrape_session_list(self):
    return ['N/A']
    