# coding: utf8
from ca_qc_montreal import MontrealPersonScraper
from utils import CanadianJurisdiction


class MontrealNord(CanadianJurisdiction):
  jurisdiction_id = u'ocd-jurisdiction/country:ca/csd:2466023/arrondissement:montréal-nord/council'
  ocd_division = u'ocd-division/country:ca/csd:2466023/arrondissement:montréal-nord'
  division_name = u'Montréal-Nord'
  name = u"Conseil d'arrondissement de Montréal-Nord"
  url = 'http://ville.montreal.qc.ca/mtlnord'
  provides = ['people']

  def get_scraper(self, term, session, scraper_type):
    if scraper_type == 'people':
        return MontrealPersonScraper
