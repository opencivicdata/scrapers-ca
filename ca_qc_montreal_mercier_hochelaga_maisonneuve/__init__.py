# coding: utf8
from ca_qc_montreal import MontrealPersonScraper
from utils import CanadianJurisdiction


class MercierHochelagaMaisonneuve(CanadianJurisdiction):
  jurisdiction_id = u'ocd-jurisdiction/country:ca/csd:2466023/arrondissement:mercier-hochelaga-maisonneuve/council'
  division_id = 'ocd-division/country:ca/csd:2466023/arrondissement:mercier-hochelaga-maisonneuve'
  division_name = u'Mercier—Hochelaga-Maisonneuve'
  name = u"Conseil d'arrondissement de Mercier—Hochelaga-Maisonneuve"
  url = 'http://ville.montreal.qc.ca/mhm'
  provides = ['people']

  def get_scraper(self, term, session, scraper_type):
    if scraper_type == 'people':
        return MontrealPersonScraper
