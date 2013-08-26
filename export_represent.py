import pymongo
import pupa_settings

def main():
  connection = pymongo.Connection(pupa_settings.MONGO_HOST, pupa_settings.MONGO_PORT)
  db = connection[pupa_settings.MONGO_DATABASE]
  for person in db['people'].find():
    person = db['people'].find_one({'_id' : member['person_id']})
    organization = db['organizations'].find_one({'_id' : member['organization_id']})
    


    data = {
      'name' : member['name'],
      'district_name' : organization['name'] + ' ' + member['post_id'],
      'elected_office' : member['role'],
      'source_url' : person['sources'][0]['url'],
      'first_name' : member['name'].split()[0],
      'last_name' : ' '.join(member['name'].split()[1:]),
      'offices' : get_offices(member['contact_details']),
      'party_name' : None,
      'email' : get_email(member['contact_details']),


    }
    

def get_email(contacts):
  for contact in contacts:
    if 'email' in contact['type']:
      return contact['value']
      break 



def get_offices(contacts):
  mapping = {
  'phone' : 'tel',
  'Phone' : 'tel',
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
  print offices



if __name__ == '__main__':
  main()
