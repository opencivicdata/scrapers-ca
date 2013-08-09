#!/usr/bin/python
# -*- coding: latin-1 -*-
from pupa.scrape import Scraper, Legislator
from larvae.person import Person
from larvae.organization import Organization

from utils import lxmlize

import re, urllib2, json, requests

COUNCIL_PAGE = 'http://depot.ville.montreal.qc.ca/bd-elus/data.json'

class MontrealPersonScraper(Scraper):
  def get_people(self):
    district = self.jurisdiction.get_metadata()["name"]
    data = urllib2.urlopen(COUNCIL_PAGE)
    data = json.load(data, 'latin-1')
    for line in data:
      if district == 'Montreal':
        if "Maire" in line['TITRE_MAIRIE'] or "Ville" in line['TITRE_CONSEIL'] or 'désigné'.decode('utf-8') in line['TITRE_CONSEIL']:
          yield self.add_councillor(line)
      elif district in remove_accents(line['ARRONDISSEMENT']):
        yield self.add_councillor(line)
  def add_councillor(self, line):
    name = line['PRENOM']+ ' ' + line['NOM']
    district = line['ARRONDISSEMENT']

    p = Legislator(name=name, district=district)
    p.add_source(COUNCIL_PAGE)

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
    return p

def remove_accents(string):
  string = string.replace('é'.decode('utf-8'),'e').replace('è'.decode('utf-8'),'e').replace('&#151;','-').replace('&#0151;','-')
  string = string.replace('Î'.decode('utf-8'),'I').replace('â'.decode('utf-8'),'a').replace('ô'.decode('utf-8'),'o')
  return string