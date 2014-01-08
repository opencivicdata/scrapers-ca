# coding: utf8
from utils import CanadianJurisdiction


class Quebec(CanadianJurisdiction):
  jurisdiction_id = u'ocd-jurisdiction/country:ca/csd:2423027/council'
  geographic_code = 2423027

  def _get_metadata(self):
    return {
      'division_name': u'Québec',
      'name': u'Conseil municipal de Québec',
      'url': 'http://www.ville.quebec.qc.ca',
    }
