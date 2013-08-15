from pupa.scrape import Jurisdiction

from .people import StCatharinesPersonScraper
from utils import lxmlize

class StCatharines(Jurisdiction):
  jurisdiction_id = 'ocd-jurisdiction/country:ca/csd:3526053/council'
  geographic_code = 3526053
  def get_metadata(self):
    return {
      'name': 'St. Catharines',
      'legislature_name': 'St. Catharines City Council',
      'legislature_url': 'http://www.stcatharines.ca/en/governin/BrianMcMullanMayor.asp',
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
        return StCatharinesPersonScraper

  def scrape_session_list(self):
    return ['N/A']
    