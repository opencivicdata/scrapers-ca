# coding: utf8
from utils import CanadianJurisdiction


class CoteSaintLuc(CanadianJurisdiction):
  jurisdiction_id = u'ocd-jurisdiction/country:ca/csd:2466058/council'
  geographic_code = 2466058

  def _get_metadata(self):
    return {
      'division_name': u'Côte-Saint-Luc',
      'name': u'Conseil municipal de Côte-Saint-Luc',
      'url': 'http://www.cotesaintluc.org',
    }
