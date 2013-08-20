# coding: utf8
from ca_qc_montreal import MontrealPersonScraper
from utils import CanadianJurisdiction


class MercierHochelagaMaisonneuve(CanadianJurisdiction):
  jurisdiction_id = 'ocd-jurisdiction/country:ca/csd:2466023/arrondissement:mercier-hochelaga-maisonneuve/council'
  ocd_division = 'ocd-division/country:ca/csd:2466023/arrondissement:mercier-hochelaga-maisonneuve'

  def _get_metadata(self):
    return {
      'name': u'Mercier—Hochelaga-Maisonneuve',
      'legislature_name': u'Mercier—Hochelaga-Maisonneuve Borough Council',
      'legislature_url': 'http://depot.ville.montreal.qc.ca/bd-elus/data.json',
      'provides': ['people'],
    }

  def get_scraper(self, term, session, scraper_type):
    if scraper_type == 'people':
        return MontrealPersonScraper
