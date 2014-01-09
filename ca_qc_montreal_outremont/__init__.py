from ca_qc_montreal import MontrealPersonScraper
from utils import CanadianJurisdiction


class Outremont(CanadianJurisdiction):
  jurisdiction_id = u'ocd-jurisdiction/country:ca/csd:2466023/arrondissement:outremont/council'
  division_id = 'ocd-division/country:ca/csd:2466023/arrondissement:outremont'
  division_name = 'Outremont'
  name = u"Conseil d'arrondissement d'Outremont"
  url = 'http://ville.montreal.qc.ca/outremont'
  provides = ['people']

  def get_scraper(self, term, session, scraper_type):
    if scraper_type == 'people':
        return MontrealPersonScraper
