from .people import MontrealPersonScraper
from utils import CanadianJurisdiction

class Montreal(CanadianJurisdiction):
  jurisdiction_id = 'ocd-jurisdiction/country:ca/csd:2466023/council'
  geographic_code = 2466023
  def _get_metadata(self):
    return {
      'name': 'Montreal',
      'legislature_name': 'Montreal City Council',
      'legislature_url': 'http://depot.ville.montreal.qc.ca/bd-elus/data.json',
      'provides': ['people'],
    }

  def get_scraper(self, term, session, scraper_type):
    if scraper_type == 'people':
        return MontrealPersonScraper

    