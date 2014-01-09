from ca_qc_montreal import MontrealPersonScraper
from utils import CanadianJurisdiction


class Verdun(CanadianJurisdiction):
  jurisdiction_id = u'ocd-jurisdiction/country:ca/csd:2466023/arrondissement:verdun/council'
  division_id = 'ocd-division/country:ca/csd:2466023/arrondissement:verdun'
  division_name = 'Verdun'
  name = u"Conseil d'arrondissement de Verdun"
  url = 'http://ville.montreal.qc.ca/verdun'
  provides = ['people']

  def get_scraper(self, term, session, scraper_type):
    if scraper_type == 'people':
        return MontrealPersonScraper
