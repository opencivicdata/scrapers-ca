# coding: utf8
import pymongo
import pupa_settings
import re
import json

def main():
  connection = pymongo.Connection(pupa_settings.MONGO_HOST, pupa_settings.MONGO_PORT)
  db = connection[pupa_settings.MONGO_DATABASE]
  i = 0

  for member in db['memberships'].find({'role' : 'member'}).sort([('jurisdiction_id', 1), ('person_id' , 1)]):
    contacts = db['memberships'].find_one({'person_id' : member['person_id']})
    person = db['people'].find_one({'_id' : member['person_id']})
    print db['organizations'].find_one({'jurisdiction_id' : member['jurisdiction_id']})['name'].__module__
     # , person['name'], member['role']



  for person in db['people'].find():
    member = db['memberships'].find_one({'person_id' : person['_id'], 'role' : {'$ne' : 'member'}})
    if not member:
      continue
      i = i+1
    # print member['jurisdiction_id']
    contacts = db['memberships'].find_one({'person_id' : person['_id'], 'role' : 'member'})
    organization = db['organizations'].find_one({'_id' : member['organization_id']})
    if person['post_id']:
      name = organization['name'] + ' ' + person['post_id']
    else:
      name = organization['name']
    name = re.sub(r'\s{2,}', ' ', name).strip()



    data = {
      'name' : person['name'],
      'district_name' : name,
      'elected_office' : member['role'],
      'source_url' : person['sources'][0]['url'],
      'offices' : get_offices(contacts['contact_details']),
      'email' : get_email(contacts['contact_details']),
      'url' : get_url(person),
      'photo_url' : person['image'],
      'personal_url' : get_personal_url(person),
      'district_id' : person['post_id'],
      'extra' : get_extra(person)

    }
    # print json.dumps(data)
    # yield json.dump(data)
  print i
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
