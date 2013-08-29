# coding: utf8
from ca_qc_montreal import MontrealPersonScraper
from utils import CanadianJurisdiction


class CoteDesNeigesNotreDameDeGrace(CanadianJurisdiction):
  jurisdiction_id = u'ocd-jurisdiction/country:ca/csd:2466023/arrondissement:côte-des-neiges-notre-dame-de-grâce/council'
  ocd_division = u'ocd-division/country:ca/csd:2466023/arrondissement:côte-des-neiges-notre-dame-de-grâce'

  def _get_metadata(self):
    return {
      'name': u'Côte-des-Neiges—Notre-Dame-de-Grâce',
      'legislature_name': u"Conseil d'arrondissement de Côte-des-Neiges—Notre-Dame-de-Grâce",
      'legislature_url': 'http://ville.montreal.qc.ca/cdn-ndg',
      'provides': ['people'],
    }

  def get_scraper(self, term, session, scraper_type):
    if scraper_type == 'people':
        return MontrealPersonScraper
