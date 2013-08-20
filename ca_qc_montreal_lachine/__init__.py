from ca_qc_montreal import MontrealPersonScraper
from utils import CanadianJurisdiction


class Lachine(CanadianJurisdiction):
  jurisdiction_id = u'ocd-jurisdiction/country:ca/csd:2466023/arrondissement:lachine/council'
  ocd_division = 'ocd-division/country:ca/csd:2466023/arrondissement:lachine'

  def _get_metadata(self):
    return {
      'name': 'Lachine',
      'legislature_name': u"Conseil d'arrondissement de Lachine",
      'legislature_url': 'http://ville.montreal.qc.ca/lachine',
      'provides': ['people'],
    }

  def get_scraper(self, term, session, scraper_type):
    if scraper_type == 'people':
        return MontrealPersonScraper
