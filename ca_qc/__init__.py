# coding: utf-8
from __future__ import unicode_literals
from utils import CanadianJurisdiction


class Quebec(CanadianJurisdiction):
    classification = 'legislature'
    division_id = 'ocd-division/country:ca/province:qc'
    division_name = 'Québec'
    name = 'Assemblée nationale du Québec'
    url = 'http://www.assnat.qc.ca'
    parties = [
        {'name': 'Parti libéral du Québec'},
        {'name': 'Parti québécois'},
        {'name': 'Coalition avenir Québec'},
        {'name': 'Québec solidaire'},
        {'name': 'Indépendante'},
    ]
