# coding: utf8
from ca_qc_montreal import MontrealPersonScraper
from utils import CanadianJurisdiction


class RosemontLaPetitePatrie(CanadianJurisdiction):
  jurisdiction_id = u'ocd-jurisdiction/country:ca/csd:2466023/arrondissement:rosemont-la_petite-patrie/council'
  division_id = 'ocd-division/country:ca/csd:2466023/arrondissement:rosemont-la_petite-patrie'
  division_name = u'Rosemont—La Petite-Patrie'
  name = u"Conseil d'arrondissement de Rosemont—La Petite-Patrie"
  url = 'http://ville.montreal.qc.ca/rpp'
  provides = ['people']

  def get_scraper(self, term, session, scraper_type):
    if scraper_type == 'people':
        return MontrealPersonScraper
