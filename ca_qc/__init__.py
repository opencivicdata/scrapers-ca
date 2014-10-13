# coding: utf-8
from __future__ import unicode_literals

from utils import CanadianJurisdiction


class Quebec(CanadianJurisdiction):
  jurisdiction_id = 'ocd-jurisdiction/country:ca/province:qc/legislature'
  geographic_code = 24
  division_name = 'Québec'
  name = 'Assemblée nationale du Québec'
  url = 'http://www.assnat.qc.ca'
  parties = [
    {'name': 'Parti libéral du Québec'},
    {'name': 'Parti québécois'},
    {'name': 'Coalition avenir Québec'},
    {'name': 'Québec solidaire'},
  ]
