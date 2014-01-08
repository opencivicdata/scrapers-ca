# coding: utf8
from utils import CanadianJurisdiction


class Levis(CanadianJurisdiction):
  jurisdiction_id = u'ocd-jurisdiction/country:ca/csd:2425213/council'
  geographic_code = 2425213

  def _get_metadata(self):
    return {
      'division_name': u'Lévis',
      'name': u'Conseil municipal de Lévis',
      'url': 'http://www.ville.levis.qc.ca',
    }
