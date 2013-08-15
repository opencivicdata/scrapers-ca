from pupa.scrape import Jurisdiction

from .people import SaskatoonPersonScraper
from utils import lxmlize

class Saskatoon(Jurisdiction):
  jurisdiction_id = 'ocd-jurisdiction/country:ca/csd:4711066/council'
  geographic_code = 4711066
  def get_metadata(self):
    return {
      'name': 'Saskatoon',
      'legislature_name': 'Saskatoon City Council',
      'legislature_url': "http://www.saskatoon.ca/CITY%20COUNCIL/YOUR%20WARD%20COUNCILLORS/Pages/default.aspx",
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
        return SaskatoonPersonScraper

  def scrape_session_list(self):
    return ['N/A']
    