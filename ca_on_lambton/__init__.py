from pupa.scrape import Jurisdiction

from .people import LambtonPersonScraper
from utils import lxmlize

class Lambton(Jurisdiction):
  jurisdiction_id = 'ca-on-lambton'

  def get_metadata(self):
    return {
      'name': 'Lambton',
      'legislature_name': 'Lambton County Council',
      'legislature_url': 'http://www.lambtononline.ca/home/government/accessingcountycouncil/countycouncillors/Pages/default.aspx',
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
        return LambtonPersonScraper

  def scrape_session_list(self):
    return ['N/A']
    