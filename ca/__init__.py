# coding: utf-8
from __future__ import unicode_literals
from utils import CanadianJurisdiction
from opencivicdata.divisions import Division
from pupa.scrape import Organization


class Canada(CanadianJurisdiction):
  classification = 'legislature'
  division_id = 'ocd-division/country:ca'
  division_name = 'Canada'
  name = 'Parliament of Canada'
  url = 'http://www.parl.gc.ca'
  parties = [
    {'name': 'Bloc Québécois'},
    {'name': 'Conservative'},
    {'name': 'Conservative Independent'},
    {'name': 'Green Party'},
    {'name': 'Independent'},
    {'name': 'Liberal'},
    {'name': 'NDP'},
  ]

  def get_organizations(self):
    parliament = Organization(self.name, classification=self.classification)
    yield parliament

    upper = Organization('Senate', classification='upper', parent_id=parliament)
    lower = Organization('House of Commons', classification='lower', parent_id=parliament)

    for division in Division.get(self.division_id).children('ed'):
      lower.add_post(role='MP', label=division.name)

    yield upper
    yield lower
