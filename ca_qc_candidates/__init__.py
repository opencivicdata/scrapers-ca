# coding: utf-8
from utils import CanadianJurisdiction


class Quebec(CanadianJurisdiction):
  jurisdiction_id = u'ocd-jurisdiction/country:ca/province:qc/legislature'
  geographic_code = 24
  division_name = u'Québec'
  name = u'Assemblée nationale du Québec'
  url = 'http://www.assnat.qc.ca'
  parties = [
    {'name': u'Coalition Avenir Québec'},
    {'name': u'Parti Québécois'},
    {'name': u'Parti libéral du Québec'},
    {'name': u'Parti vert du Québec'},
    {'name': u'Québec solidaire'},
  ]
