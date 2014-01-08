from ca_qc_montreal import MontrealPersonScraper
from utils import CanadianJurisdiction


class LaSalle(CanadianJurisdiction):
  jurisdiction_id = u'ocd-jurisdiction/country:ca/csd:2466023/arrondissement:lasalle/council'
  ocd_division = 'ocd-division/country:ca/csd:2466023/arrondissement:lasalle'
  division_name = 'LaSalle'
  name = u"Conseil d'arrondissement de LaSalle"
  url = 'http://ville.montreal.qc.ca/lasalle'
  provides = ['people']

  def get_scraper(self, term, session, scraper_type):
    if scraper_type == 'people':
        return MontrealPersonScraper
