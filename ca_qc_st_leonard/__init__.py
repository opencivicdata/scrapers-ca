#coding: utf8
from ca_qc_montreal import MontrealPersonScraper
from utils import CanadianJurisdiction

class St_Leonard(CanadianJurisdiction):
  jurisdiction_id = 'ca-qc-st-leonard'

  def _get_metadata(self):
    return {
      'name': u'Saint-Léonard',
      'legislature_name': u'Saint-Léonard Borough Council',
      'legislature_url': 'http://depot.ville.montreal.qc.ca/bd-elus/data.json',
      'provides': ['people'],
    }

  def get_scraper(self, term, session, scraper_type):
    if scraper_type == 'people':
        return MontrealPersonScraper
