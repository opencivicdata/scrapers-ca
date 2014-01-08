from ca_qc_montreal import MontrealPersonScraper
from utils import CanadianJurisdiction


class SaintLaurent(CanadianJurisdiction):
  jurisdiction_id = u'ocd-jurisdiction/country:ca/csd:2466023/arrondissement:saint-laurent/council'
  ocd_division = 'ocd-division/country:ca/csd:2466023/arrondissement:saint-laurent'

  def _get_metadata(self):
    return {
      'division_name': 'Saint-Laurent',
      'name': u"Conseil d'arrondissement de Saint-Laurent",
      'url': 'http://ville.montreal.qc.ca/saint-laurent',
      'provides': ['people'],
    }

  def get_scraper(self, term, session, scraper_type):
    if scraper_type == 'people':
        return MontrealPersonScraper
