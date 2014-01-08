# coding: utf8
from utils import CanadianJurisdiction


class SaintJerome(CanadianJurisdiction):
  jurisdiction_id = u'ocd-jurisdiction/country:ca/csd:2475017/council'
  geographic_code = 2475017

  def _get_metadata(self):
    return {
      'division_name': u'Saint-Jérôme',
      'name': u'Conseil municipal de Saint-Jérôme',
      'url': 'http://www.ville.saint-jerome.qc.ca',
    }
