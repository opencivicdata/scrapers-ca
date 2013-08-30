# coding: utf8
import pymongo
import pupa_settings
import re
import json
import os
import importlib
import pupa.core
from pupa.core import db


def main():
  pupa.core._configure_db(os.environ['MONGOHQ_URL'], 27017, 'app17409961')
  for module_name in os.listdir('./mycityhall_scrapers/'):
    if os.path.isdir('./mycityhall_scrapers/'+module_name) and module_name not in ('.git', '.gitignore', '.profile.d', '.heroku' , 'scrape_cache', 'scraped_data', 'represent_data'):
      module = importlib.import_module(module_name)
      for obj in module.__dict__.values():
        jurisdiction_id = getattr(obj, 'jurisdiction_id', None)
        if jurisdiction_id:  # We've found the module.
          with open(os.path.abspath(os.path.join(__file__, os.pardir)) + '/represent_data/'+module_name+'.json', 'w') as json_file:
            content = []
            for member in db.memberships.find({'jurisdiction_id' : jurisdiction_id, 'role' : 'member'}):
              organization = db.organizations.find_one({'_id' : member['organization_id']})
              person = db.people.find_one({'_id' : member['person_id']})
              role = db.memberships.find_one({'person_id': member['person_id'], 'role' : {'$ne' : 'member'}})
              if role:
                role = role['role']
              else:
                role = 'councillor'

              name = organization['name'] + ' ' + person['post_id']
              data = {
                'name' : person['name'],
                'district_name' : name,
                'elected_office' : member['role'],
                'source_url' : person['sources'][0]['url'],
                'offices' : get_offices(member['contact_details']),
                'email' : get_email(member['contact_details']),
                'url' : get_url(person),
                'photo_url' : person['image'],
                'personal_url' : get_personal_url(person),
                'district_id' : person['post_id'],
                'extra' : get_extra(person)
              }
              content.append(data)
            json.dump(content, json_file)


def get_extra(person):
  extra = {}
  for link in person['links']:
    if not 'personal' in link['note']:
      extra[link['note']] = link['url']
  return extra

def get_personal_url(person):
  for link in person['links']:
    if 'personal' in link['note'] or 'site' in link['note'] or 'Website' in link['note']:
      return link['url']
  return None

def get_url(person):
  if len(person['sources']) == 1:
    return person['sources'][0]['url']
  else:
    return person['sources'][1]['url']

def get_email(contacts):
  for contact in contacts:
    if 'email' in contact['type'] or 'Email' in contact['type']:
      return contact['value']
      break
  return None 



def get_offices(contacts):
  mapping = {
  'phone' : 'tel',
  'Phone' : 'tel',
  'Telephone' : 'tel',
  'Address' : 'postal',
  'address' : 'postal',
  'Fax' : 'fax',
  'fax' : 'fax',
  }


  offices = []
  office_types = []
  for contact in contacts:
    office_types.append(contact['note'])
  office_types = sorted(set(office_types))
  
  
  for office_type in office_types:
    offices.append({'type' : office_type})
  
  for contact in contacts:
    if 'mail' in contact['type']:
      continue
    for i, office_type in enumerate(office_types):
      if contact['note'] == office_type:
        offices[i][mapping[contact['type']]] = contact['value']
  return offices



if __name__ == '__main__':
  main()
