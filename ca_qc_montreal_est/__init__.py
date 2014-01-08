# coding: utf8
from utils import CanadianJurisdiction


class MontrealEst(CanadianJurisdiction):
  jurisdiction_id = u'ocd-jurisdiction/country:ca/csd:2466007/council'
  geographic_code = 2466007

  def _get_metadata(self):
    return {
      'division_name': u'Montréal-Est',
      'name': u'Conseil municipal de Montréal-Est',
      'url': 'http://ville.montreal-est.qc.ca',
    }
