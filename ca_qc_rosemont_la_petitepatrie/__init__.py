# coding: utf8
from ca_qc_montreal import MontrealPersonScraper
from utils import CanadianJurisdiction


class Rosemont_La_Petite_Patrie(CanadianJurisdiction):
  jurisdiction_id = 'ca-qc-rosemont-la_petitepatrie'
  ocd_division = 'ocd-division/country:ca/csd:2466023/arrondissement:rosemont-la_petite-patrie'

  def _get_metadata(self):
    return {
      'name': u'Rosemont—La Petite-Patrie',
      'legislature_name': u'Rosemont—La Petite-Patrie Borough Council',
      'legislature_url': 'http://depot.ville.montreal.qc.ca/bd-elus/data.json',
      'provides': ['people'],
    }

  def get_scraper(self, term, session, scraper_type):
    if scraper_type == 'people':
        return MontrealPersonScraper
