# coding: utf8
from utils import CanadianJurisdiction


class Lévis(CanadianJurisdiction):
  jurisdiction_id = u'ocd-jurisdiction/country:ca/csd:2425213/council'
  geographic_code = 2425213

  def _get_metadata(self):
    return {
      'name': u'Lévis',
      'legislature_name': u'Conseil municipal de Lévis',
      'legislature_url': 'http://www.ville.levis.qc.ca',
    }
