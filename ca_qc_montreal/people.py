# -*- coding: utf-8== -*-
from pupa.scrape import Scraper, Legislator

from utils import lxmlize, CanadianScraper

import re
import urllib2
import json
import requests

COUNCIL_PAGE = 'http://depot.ville.montreal.qc.ca/bd-elus/data.json'


class MontrealPersonScraper(CanadianScraper):

  def get_people(self):
    organization = self.get_organization()
    yield organization

    district = self.jurisdiction.get_metadata()["name"]
    data = urllib2.urlopen(COUNCIL_PAGE)
    data = json.load(data, 'latin-1')
    for line in data:
      if district == u'Montréal':
        if "Maire" in line['TITRE_MAIRIE'] or "Ville" in line['TITRE_CONSEIL'] or 'désigné'.decode('utf-8') in line['TITRE_CONSEIL']:
          yield self.add_councillor(line, organization)
      elif district in format(line['ARRONDISSEMENT']):
        yield self.add_councillor(line, organization)

  def add_councillor(self, line, organization):
    name = line['PRENOM'] + ' ' + line['NOM']
    district = line['ARRONDISSEMENT']

    p = Legislator(name=name, post_id=district)
    p.add_source(COUNCIL_PAGE)

    if line['TITRE_MAIRIE']:
      p.add_membership(organization, role='mayor')
    else:
      p.add_membership(organization, role='councillor')
    if line['ADRESSE_ARRONDISSEMENT']:
      p.add_contact('address', line['ADRESSE_ARRONDISSEMENT'], 'district')
    if line['ADRESSE_HOTEL_DE_VILLE']:
      p.add_contact('address', line['ADRESSE_HOTEL_DE_VILLE'], 'city')
    if line['TELEPHONE_ARRONDISSEMENT']:
      p.add_contact('phone', line['TELEPHONE_ARRONDISSEMENT'], 'district')
    if line['TELEPHONE_HOTEL_DE_VILLE']:
      p.add_contact('phone', line['TELEPHONE_HOTEL_DE_VILLE'], 'city')
    if line['TELECOPIE_ARRONDISSEMENT']:
      p.add_contact('fax', line['TELECOPIE_ARRONDISSEMENT'], 'district')
    if line['COURRIEL']:
      p.add_contact('email', line['COURRIEL'], None)
    if line['FICHIER_IMAGE']:
      p.image = line['FICHIER_IMAGE']
    return p


def format(string):
  return unicode(re.sub(r'&#0?151;', u'-', unicode(string)))
