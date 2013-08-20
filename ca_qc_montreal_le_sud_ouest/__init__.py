from ca_qc_montreal import MontrealPersonScraper
from utils import CanadianJurisdiction


class LeSudOuest(CanadianJurisdiction):
  jurisdiction_id = 'ocd-jurisdiction/country:ca/csd:2466023/arrondissement:le_sud-ouest/council'
  ocd_division = 'ocd-division/country:ca/csd:2466023/arrondissement:le_sud-ouest'

  def _get_metadata(self):
    return {
      'name': 'Le Sud-Ouest',
      'legislature_name': 'Sud-Ouest Borough Council',
      'legislature_url': 'http://depot.ville.montreal.qc.ca/bd-elus/data.json',
      'provides': ['people'],
    }

  def get_scraper(self, term, session, scraper_type):
    if scraper_type == 'people':
        return MontrealPersonScraper
