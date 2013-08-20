# coding: utf8
from utils import CanadianJurisdiction


class MontrealEst(CanadianJurisdiction):
  jurisdiction_id = 'ocd-jurisdiction/country:ca/csd:2466007/council'
  geographic_code = 2466007

  def _get_metadata(self):
    return {
      'name': u'Montréal-Est',
      'legislature_name': u'Conseil municipal de Montréal-Est',
      'legislature_url': 'http://ville.montreal-est.qc.ca',
    }
