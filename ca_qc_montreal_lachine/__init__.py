from ca_qc_montreal import MontrealPersonScraper
from utils import CanadianJurisdiction


class Lachine(CanadianJurisdiction):
  jurisdiction_id = 'ocd-jurisdiction/country:ca/csd:2466023/arrondissement:lachine/council'
  ocd_division = 'ocd-division/country:ca/csd:2466023/arrondissement:lachine'

  def _get_metadata(self):
    return {
      'name': 'Lachine',
      'legislature_name': 'Lachine Borough Council',
      'legislature_url': 'http://depot.ville.montreal.qc.ca/bd-elus/data.json',
      'provides': ['people'],
    }

  def get_scraper(self, term, session, scraper_type):
    if scraper_type == 'people':
        return MontrealPersonScraper
