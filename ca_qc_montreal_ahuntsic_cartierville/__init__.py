from ca_qc_montreal import MontrealPersonScraper
from utils import CanadianJurisdiction


class AhuntsicCartierville(CanadianJurisdiction):
  jurisdiction_id = u'ocd-jurisdiction/country:ca/csd:2466023/arrondissement:ahuntsic-cartierville/council'
  ocd_division = 'ocd-division/country:ca/csd:2466023/arrondissement:ahuntsic-cartierville'

  def _get_metadata(self):
    return {
      'division_name': 'Ahuntsic-Cartierville',
      'name': u"Conseil d'arrondissement d'Ahuntsic-Cartierville",
      'url': 'http://ville.montreal.qc.ca/ahuntsic-cartierville',
      'provides': ['people'],
    }

  def get_scraper(self, term, session, scraper_type):
    if scraper_type == 'people':
        return MontrealPersonScraper
