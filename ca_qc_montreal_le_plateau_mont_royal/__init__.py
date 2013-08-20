from ca_qc_montreal import MontrealPersonScraper
from utils import CanadianJurisdiction


class LePlateauMontRoyal(CanadianJurisdiction):
  jurisdiction_id = 'ocd-jurisdiction/country:ca/csd:2466023/arrondissement:le_plateau-mont-royal/council'
  ocd_division = 'ocd-division/country:ca/csd:2466023/arrondissement:le_plateau-mont-royal'

  def _get_metadata(self):
    return {
      'name': 'Le Plateau-Mont-Royal',
      'legislature_name': u"Conseil d'arrondissement de legislature_name': 'Le Plateau-Mont-Royal",
      'legislature_url': 'http://ville.montreal.qc.ca/plateau',
      'provides': ['people'],
    }

  def get_scraper(self, term, session, scraper_type):
    if scraper_type == 'people':
        return MontrealPersonScraper
