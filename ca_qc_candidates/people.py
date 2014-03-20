# coding: utf-8
from pupa.scrape import Scraper

from utils import csv_reader, CanadianLegislator as Legislator

import re

COUNCIL_PAGE = 'https://docs.google.com/spreadsheet/pub?key=0Ao14DXi7q85PdDJ2cnhwdjU4Um1mMGtFeFN1aGI5QlE&single=true&gid=0&output=csv'


KEYS = {
  'District Name': 'post_id',
  'Full Name': 'name',
  'Party Name': 'party',
  'Gender': 'gender',
}
IGNORE_KEYS = set((
  'First Name',
  'Last Name',
))
CONTACT_TYPE_KEYS = {
  'Telephone': 'voice',
  'Fax': 'fax',
  'Postal Address': 'address',
}
LINKS_KEYS = set((
  "Incumbent's Legislative URL",
  "Personal URL",
  "Campaign Website URL",
  "Photo URL",
))
EXTRA_KEYS = set((
  'Incumbent?',
  'Twitter',
  'Facebook',
  'Instagram',
  'Flickr',
))


class QuebecPersonScraper(Scraper):

  def get_people(self):
    reader = csv_reader(COUNCIL_PAGE, header=True)
    for row in reader:
      kwargs = {'role': 'candidate'}
      email = None
      links = []
      extra = {}
      offices = []

      for k, v in row.items():
        v = v.strip()
        if not v:
          continue

        k = k.strip()
        match = re.search(r'\AOffice (\d): ', k)
        if match:
          index = int(match.group(1))
          while index > len(offices):
            offices.append({})
          if k[10:] == 'Type':
            offices[index - 1]['note'] = v
          elif k[10:] in CONTACT_TYPE_KEYS:
            offices[index - 1][CONTACT_TYPE_KEYS[k[10:]]] = v
          else:
            raise Exception(k)
        elif k in KEYS:
          kwargs[KEYS[k]] = v
        elif k == 'Email':
          email = v
        elif k in LINKS_KEYS:
          links.append({'url': v, 'note': k})
        elif k in IGNORE_KEYS:
          continue
        elif k in EXTRA_KEYS:
          extra[re.sub(r'[^a-z0-9_]', '', k.lower().replace(' ', '_'))] = v
        else:
          raise Exception(k)

      contacts = []
      for office in offices:
        for _, type in CONTACT_TYPE_KEYS.items():
          if office.get(type):
            contacts.push({'note': office['note'], type: type, 'value': office[type]})

      if 'name' in kwargs:
        if kwargs.get('party') == u'Québec Solidaire':
          kwargs['party'] = u'Québec solidaire'

        p = Legislator(**kwargs)
        p.add_source(COUNCIL_PAGE)
        if email:
          p.add_contact('email', email, None)
        for link in links:
          p.add_link(**links)
        for contact in contacts:
          p.add_contact(**contact)
        for k, v in extra.items():
          p.add_extra(k, v)
        yield p
