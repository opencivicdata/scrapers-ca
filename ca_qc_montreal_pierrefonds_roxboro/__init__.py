from ca_qc_montreal import MontrealPersonScraper
from utils import CanadianJurisdiction


class PierrefondsRoxboro(CanadianJurisdiction):
  jurisdiction_id = u'ocd-jurisdiction/country:ca/csd:2466023/arrondissement:pierrefonds-roxboro/council'
  division_id = 'ocd-division/country:ca/csd:2466023/arrondissement:pierrefonds-roxboro'
  division_name = 'Pierrefonds-Roxboro'
  name = u"Conseil d'arrondissement de Pierrefonds-Roxboro"
  url = 'http://ville.montreal.qc.ca/pierrefonds-roxboro'
  provides = ['people']

  def get_scraper(self, term, session, scraper_type):
    if scraper_type == 'people':
        return MontrealPersonScraper
