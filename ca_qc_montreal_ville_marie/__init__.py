from ca_qc_montreal import MontrealPersonScraper
from utils import CanadianJurisdiction


class VilleMarie(CanadianJurisdiction):
  jurisdiction_id = 'ocd-jurisdiction/country:ca/csd:2466023/arrondissement:ville-marie/council'
  ocd_division = 'ocd-division/country:ca/csd:2466023/arrondissement:ville-marie'

  def _get_metadata(self):
    return {
      'name': 'Ville-Marie',
      'legislature_name': 'Ville-Marie Borough Council',
      'legislature_url': 'http://depot.ville.montreal.qc.ca/bd-elus/data.json',
      'provides': ['people'],
    }

  def get_scraper(self, term, session, scraper_type):
    if scraper_type == 'people':
        return MontrealPersonScraper
