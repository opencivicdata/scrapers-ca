from ca_qc_montreal import MontrealPersonScraper
from utils import CanadianJurisdiction


class SaintLaurent(CanadianJurisdiction):
  jurisdiction_id = 'ocd-jurisdiction/country:ca/csd:2466023/arrondissement:saint-laurent/council'
  ocd_division = 'ocd-division/country:ca/csd:2466023/arrondissement:saint-laurent'

  def _get_metadata(self):
    return {
      'name': 'Saint-Laurent',
      'legislature_name': u"Conseil d'arrondissement de Saint-Laurent",
      'legislature_url': 'http://ville.montreal.qc.ca/saint-laurent',
      'provides': ['people'],
    }

  def get_scraper(self, term, session, scraper_type):
    if scraper_type == 'people':
        return MontrealPersonScraper
