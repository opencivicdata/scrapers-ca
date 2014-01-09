from ca_qc_montreal import MontrealPersonScraper
from utils import CanadianJurisdiction


class LeSudOuest(CanadianJurisdiction):
  jurisdiction_id = u'ocd-jurisdiction/country:ca/csd:2466023/arrondissement:le_sud-ouest/council'
  division_id = 'ocd-division/country:ca/csd:2466023/arrondissement:le_sud-ouest'
  division_name = 'Le Sud-Ouest'
  name = u"Conseil d'arrondissement du Sud-Ouest"
  url = 'http://ville.montreal.qc.ca/sud-ouest'
  provides = ['people']

  def get_scraper(self, term, session, scraper_type):
    if scraper_type == 'people':
        return MontrealPersonScraper
