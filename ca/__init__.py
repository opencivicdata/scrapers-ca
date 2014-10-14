# coding: utf-8
from __future__ import unicode_literals
from utils import CanadianJurisdiction
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
    parent = Organization('Parliament of Canada', classification='legislature')
    yield parent
    yield Organization('House of Commons', classification='lower', parent_id=parent)
    yield Organization('Senate', classification='upper', parent_id=parent)
