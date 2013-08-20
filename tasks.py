# coding: utf8

import importlib
import codecs
import os
import os.path
import re
import string

from git import Repo
import lxml.html
import requests
from unidecode import unidecode

# Reads a remote CSV file.
def csv_reader(url):
  import csv
  from StringIO import StringIO
  return csv.reader(StringIO(requests.get(url).content))

# Map Standard Geographical Classification codes to the OCD identifiers of provinces and territories.
province_and_territory_codes = {}
reader = csv_reader('https://raw.github.com/opencivicdata/ocd-division-ids/master/mappings/country-ca-sgc/ca_provinces_and_territories.csv')
for row in reader:
  province_and_territory_codes[row[1]] = row[0]

# Map OCD identifiers to URLs.
urls = {}
reader = csv_reader('https://raw.github.com/jpmckinney/ocd-division-ids/ca/mappings/country-ca-urls/ca_census_subdivisions.csv') # @todo switch repository and branch
for row in reader:
  urls[row[0].decode('utf8')] = row[1]
reader = csv_reader('https://raw.github.com/jpmckinney/ocd-division-ids/ca/mappings/country-ca-urls/census_subdivision-montreal-arrondissements.csv') # @todo switch repository and branch
for row in reader:
  urls[row[0].decode('utf8')] = row[1]

# Map census subdivision type codes to names.
census_subdivision_type_names = {}
document = lxml.html.fromstring(requests.get('http://www12.statcan.gc.ca/census-recensement/2011/ref/dict/table-tableau/table-tableau-5-eng.cfm').content)
for abbr in document.xpath('//table/tbody/tr/th[1]/abbr'):
  census_subdivision_type_names[abbr.text_content()] = re.sub(' /.+\Z', '', abbr.attrib['title'])

# Map OCD identifiers to census subdivision types.
census_subdivision_types = {}
reader = csv_reader('https://raw.github.com/opencivicdata/ocd-division-ids/master/mappings/country-ca-types/ca_census_subdivisions.csv')
for row in reader:
  census_subdivision_types[row[0]] = census_subdivision_type_names[row[1].decode('utf8')]

# Map OCD identifiers and Standard Geographical Classification codes to names.
names = {}
reader = csv_reader('https://raw.github.com/jpmckinney/ocd-division-ids/ca/identifiers/country-ca/census_subdivision-montreal-arrondissements.csv') # @todo switch repository and branch
for row in reader:
  names[row[0].decode('utf8')] = row[1].decode('utf8')
reader = csv_reader('https://raw.github.com/opencivicdata/ocd-division-ids/master/identifiers/country-ca/ca_provinces_and_territories.csv')
for row in reader:
  names[row[0].decode('utf8')] = row[1].decode('utf8')
reader = csv_reader('https://raw.github.com/opencivicdata/ocd-division-ids/master/identifiers/country-ca/ca_census_subdivisions.csv')
for row in reader:
  names[row[0].decode('utf8')] = row[1].decode('utf8')

repo = Repo('.')
index = repo.index

def slug(ocd_division):
  return unidecode(unicode(names[ocd_division]).lower().translate({
    ord(u' '): u'_',
    ord(u"'"): u'_',
    ord(u'-'): u'_', # dash
    ord(u'—'): u'_', # m-dash
    ord(u'–'): u'_', # n-dash
    ord(u'.'): None,
  }))

for module_name in os.listdir('.'):
  jurisdiction_ids = set()
  ocd_divisions = set()

  if os.path.isdir(module_name) and module_name not in ('.git', 'scrape_cache', 'scraped_data'):
    module = importlib.import_module(module_name)
    for obj in module.__dict__.values():
      jurisdiction_id = getattr(obj, 'jurisdiction_id', None)
      if jurisdiction_id:  # We've found the module.
        # Ensure jurisdiction_id is unique.
        if jurisdiction_id in jurisdiction_ids:
          raise Exception('Duplicate jurisdiction_id %s' % jurisdiction_id)
        else:
          jurisdiction_ids.add(jurisdiction_id)

        ocd_division = getattr(obj, 'ocd_division', None)
        geographic_code = getattr(obj, 'geographic_code', None)
        if ocd_division:
          if geographic_code:
            raise Exception('%s: Set ocd_division or geographic_code' % module_name)
        else:
          if geographic_code:
            geographic_code = str(geographic_code)
            length = len(geographic_code)
            if length == 2:
              ocd_division = province_and_territory_codes[geographic_code]
            elif length == 7:
              ocd_division = 'ocd-division/country:ca/csd:%s' % geographic_code
            else:
              raise Exception('%s: Unrecognized geographic code %s' % (module_name, geographic_code))

        if ocd_division:
          # Ensure ocd_division is unique.
          if ocd_division in ocd_divisions:
            raise Exception('%s: Duplicate ocd_division %s' % (module_name, ocd_division))
          else:
            ocd_divisions.add(ocd_division)

            instance = obj()
          sections = ocd_division.split('/')
          ocd_type, ocd_type_id = sections[-1].split(':')

          # Determine the expected module name, class name and jurisdiction_id.
          if ocd_type in ('province', 'territory'):
            expected_module_name = 'ca_%s' % ocd_type_id
            if ocd_type_id in ('nl', 'ns'):
              expected_legislature_name = '%s House of Assembly' % names[ocd_division]
            else:
              expected_legislature_name = 'Legislative Assembly of %s' % names[ocd_division]
            jurisdiction_id_suffix = 'legislature'
          elif ocd_type == 'csd':
            province_or_territory_type_id = province_and_territory_codes[ocd_type_id[:2]].split(':')[-1]
            expected_module_name = 'ca_%s_%s' % (province_or_territory_type_id, slug(ocd_division))
            if ocd_type_id[:2] == '24':
              expected_legislature_name = 'Conseil municipal de %s' % names[ocd_division]
            else:
              legislature_name_infix = census_subdivision_types[ocd_division]
              if legislature_name_infix in ('Municipality', 'Specialized municipality'):
                legislature_name_infix = 'Municipal'
              elif legislature_name_infix == 'Regional municipality':
                legislature_name_infix = 'Regional'
              expected_legislature_name = '%s %s Council' % (names[ocd_division], legislature_name_infix)
            jurisdiction_id_suffix = 'council'
          elif ocd_type == 'arrondissement':
            census_subdivision_type_id = sections[-2].split(':')[-1]
            province_or_territory_type_id = province_and_territory_codes[census_subdivision_type_id[:2]].split(':')[-1]
            expected_module_name = 'ca_%s_%s_%s' % (province_or_territory_type_id, slug('/'.join(sections[:-1])), slug(ocd_division))
            if names[ocd_division][0] in ('A', 'E', 'I', 'O', 'U'):
              expected_legislature_name = "Conseil d'arrondissement d'%s" % names[ocd_division]
            elif names[ocd_division][:3] == 'Le ':
              expected_legislature_name = "Conseil d'arrondissement du %s" % names[ocd_division][3:]
            else:
              expected_legislature_name = "Conseil d'arrondissement de %s" % names[ocd_division]
            jurisdiction_id_suffix = 'council'
          else:
            raise Exception('%s: Unrecognized OCD type %s' % (module_name, ocd_type))
          class_name_parts = re.split('[ -]', re.sub(u"[—–]", '-', re.sub("['.]", '', names[ocd_division])))
          expected_class_name = unidecode(unicode(''.join(word if re.match('[A-Z]', word) else word.capitalize() for word in class_name_parts)))
          expected_jurisdiction_id = ocd_division.replace('ocd-division', 'ocd-jurisdiction') + '/' + jurisdiction_id_suffix

          # Warn if there is no expected legislative URL.
          legislature_url = instance.metadata['legislature_url']
          expected_legislature_url = None
          if urls.get(ocd_division):
            expected_legislature_url = urls[ocd_division]
          else:
            print '%-60s %s' % (module_name, legislature_url)

          # Warn if the legislature_name may be incorrect.
          legislature_name = instance.metadata['legislature_name']
          if legislature_name != expected_legislature_name:
            print '%-60s %s' % (legislature_name, expected_legislature_name)

          # Name the classes correctly.
          class_name = obj.__name__
          if class_name != expected_class_name:
            for basename in os.listdir(module_name):
              if basename.endswith('.py'):
                with codecs.open(os.path.join(module_name, basename), 'r', 'utf8') as f:
                  content = f.read()
                with codecs.open(os.path.join(module_name, basename), 'w', 'utf8') as f:
                  content = content.replace(class_name, expected_class_name)
                  f.write(content)

          # Set the name, jurisdiction_id and legislature_url appropriately.
          name = instance.metadata['name']
          expected_name = names[ocd_division]
          if name != expected_name or jurisdiction_id != expected_jurisdiction_id or (expected_legislature_url and legislature_url != expected_legislature_url):
           with codecs.open(os.path.join(module_name, '__init__.py'), 'r', 'utf8') as f:
              content = f.read()
           with codecs.open(os.path.join(module_name, '__init__.py'), 'w', 'utf8') as f:
              if name != expected_name:
                content = content.replace(name, expected_name)
              if jurisdiction_id != expected_jurisdiction_id:
                content = content.replace(jurisdiction_id, expected_jurisdiction_id)
              if expected_legislature_url and legislature_url != expected_legislature_url:
                content = content.replace(legislature_url, expected_legislature_url)
              f.write(content)

          # Name the module correctly.
          if module_name != expected_module_name:
            index.move([module_name, expected_module_name])
        else:
          print 'No OCD division for %s' % module_name

# @todo
# legislature_url: compare to sources in scraped data
# fix all the jurisdictions without geographic_code, especially the pseudo-jurisdictions
