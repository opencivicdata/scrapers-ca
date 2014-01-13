# coding: utf8
from pupa.scrape import Scraper, Legislator

from utils import lxmlize, CanadianScraper

import re
import urllib2
import json
import requests

COUNCIL_PAGE = 'http://depot.ville.montreal.qc.ca/bd-elus/data.json'


class MontrealPersonScraper(CanadianScraper):

  def get_people(self):
    district = self.jurisdiction.name
    data = urllib2.urlopen(COUNCIL_PAGE)
    data = json.load(data, 'windows-1252')
    for line in data:
      if district == u'Montréal':
        if "Maire" in line['TITRE_MAIRIE'] or "Ville" in line['TITRE_CONSEIL'] or 'désigné'.decode('utf-8') in line['TITRE_CONSEIL']:
          yield self.add_councillor(line)
      elif district in format(line['ARRONDISSEMENT']):
        yield self.add_councillor(line)

  def add_councillor(self, line):
    name = line['PRENOM'] + ' ' + line['NOM']
    district = line['ARRONDISSEMENT']

    p = Legislator(name=name, post_id=district)
    p.add_source(COUNCIL_PAGE)

    if line['TITRE_MAIRIE']:
      p.role = 'Mayor'
    else:
      p.role = 'Councillor'
    if line['ADRESSE_ARRONDISSEMENT']:
      p.add_contact('address', line['ADRESSE_ARRONDISSEMENT'], 'legislature')
    if line['ADRESSE_HOTEL_DE_VILLE']:
      p.add_contact('address', line['ADRESSE_HOTEL_DE_VILLE'], 'legislature')
    if line['TELEPHONE_ARRONDISSEMENT']:
      p.add_contact('voice', line['TELEPHONE_ARRONDISSEMENT'], 'legislature')
    if line['TELEPHONE_HOTEL_DE_VILLE']:
      p.add_contact('voice', line['TELEPHONE_HOTEL_DE_VILLE'], 'legislature')
    if line['TELECOPIE_ARRONDISSEMENT']:
      p.add_contact('fax', line['TELECOPIE_ARRONDISSEMENT'], 'legislature')
    if line['TELECOPIE_HOTEL_DE_VILLE']:
      p.add_contact('fax', line['TELECOPIE_HOTEL_DE_VILLE'], 'legislature')
    if line['COURRIEL']:
      p.add_contact('email', line['COURRIEL'], None)
    if line['FICHIER_IMAGE']:
      p.image = line['FICHIER_IMAGE']
    return p


def format(string):
  return unicode(re.sub(r'&#0?151;', u'—', unicode(string).replace(u'–', u'-')))  # replace n-dash with dash, unencode m-dash
