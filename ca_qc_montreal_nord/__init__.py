# coding: utf8
from ca_qc_montreal import MontrealPersonScraper
from utils import CanadianJurisdiction


class Montreal_Nord(CanadianJurisdiction):
  jurisdiction_id = u'ca-qc-montreal-nord'
  ocd_division = u'ocd-division/country:ca/csd:2466023/arrondissement:montréal-nord'

  def _get_metadata(self):
    return {
      'name': u'Montréal-Nord',
      'legislature_name': u"Conseil d'arrondissement de Montréal-Nord",
      'legislature_url': 'http://ville.montreal.qc.ca/mtlnord',
      'provides': ['people'],
    }

  def get_scraper(self, term, session, scraper_type):
    if scraper_type == 'people':
        return MontrealPersonScraper
