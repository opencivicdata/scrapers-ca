# coding: utf8
from ca_qc_montreal import MontrealPersonScraper
from utils import CanadianJurisdiction


class MercierHochelagaMaisonneuve(CanadianJurisdiction):
  jurisdiction_id = u'ocd-jurisdiction/country:ca/csd:2466023/arrondissement:mercier-hochelaga-maisonneuve/council'
  ocd_division = 'ocd-division/country:ca/csd:2466023/arrondissement:mercier-hochelaga-maisonneuve'

  def _get_metadata(self):
    return {
      'name': u'Mercier-Hochelaga-Maisonneuve',
      'legislature_name': u"Conseil d'arrondissement de Mercier—Hochelaga-Maisonneuve",
      'legislature_url': 'http://ville.montreal.qc.ca/mhm',
      'provides': ['people'],
    }

  def get_scraper(self, term, session, scraper_type):
    if scraper_type == 'people':
        return MontrealPersonScraper
