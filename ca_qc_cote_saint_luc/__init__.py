# coding: utf8
from utils import CanadianJurisdiction


class CoteSaintLuc(CanadianJurisdiction):
  jurisdiction_id = 'ocd-jurisdiction/country:ca/csd:2466058/council'
  geographic_code = 2466058

  def _get_metadata(self):
    return {
      'name': u'Côte-Saint-Luc',
      'legislature_name': u'Conseil municipal de Côte-Saint-Luc',
      'legislature_url': 'http://www.cotesaintluc.org/Administration',
    }
