from ca_qc_montreal import MontrealPersonScraper
from utils import CanadianJurisdiction


class Lachine(CanadianJurisdiction):
  jurisdiction_id = u'ocd-jurisdiction/country:ca/csd:2466023/arrondissement:lachine/council'
  division_id = 'ocd-division/country:ca/csd:2466023/arrondissement:lachine'
  division_name = 'Lachine'
  name = u"Conseil d'arrondissement de Lachine"
  url = 'http://ville.montreal.qc.ca/lachine'
  provides = ['people']

  def get_scraper(self, term, session, scraper_type):
    if scraper_type == 'people':
        return MontrealPersonScraper
