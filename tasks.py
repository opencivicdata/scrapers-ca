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

# Tidies all scraper code.


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
reader = csv_reader('https://raw.github.com/opencivicdata/ocd-division-ids/master/mappings/country-ca-urls/ca_census_subdivisions.csv')
for row in reader:
  urls[row[0].decode('utf8')] = row[1]
reader = csv_reader('https://raw.github.com/opencivicdata/ocd-division-ids/master/mappings/country-ca-urls/census_subdivision-montreal-arrondissements.csv')
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
reader = csv_reader('https://raw.github.com/opencivicdata/ocd-division-ids/master/identifiers/country-ca/census_subdivision-montreal-arrondissements.csv')
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


def slug(division_id):
  return unidecode(unicode(names[division_id]).lower().translate({
    ord(u' '): u'_',
    ord(u"'"): u'_',
    ord(u'-'): u'_',  # dash
    ord(u'—'): u'_',  # m-dash
    ord(u'–'): u'_',  # n-dash
    ord(u'.'): None,
  }))

for module_name in os.listdir('.'):
  jurisdiction_ids = set()
  division_ids = set()

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

        # Determine the division_id.
        division_id = getattr(obj, 'division_id', None)
        geographic_code = getattr(obj, 'geographic_code', None)
        if division_id:
          if geographic_code:
            raise Exception('%s: Set division_id or geographic_code' % module_name)
        else:
          if geographic_code:
            geographic_code = str(geographic_code)
            length = len(geographic_code)
            if length == 2:
              division_id = province_and_territory_codes[geographic_code]
            elif length == 7:
              division_id = 'ocd-division/country:ca/csd:%s' % geographic_code
            else:
              raise Exception('%s: Unrecognized geographic code %s' % (module_name, geographic_code))

        if division_id:
          # Ensure division_id is unique.
          if division_id in division_ids:
            raise Exception('%s: Duplicate division_id %s' % (module_name, division_id))
          else:
            division_ids.add(division_id)

          sections = division_id.split('/')
          ocd_type, ocd_type_id = sections[-1].split(':')

          # Determine the expected module name and jurisdiction_id.
          if ocd_type in ('province', 'territory'):
            expected_module_name = 'ca_%s' % ocd_type_id
            if ocd_type_id in ('nl', 'ns'):
              expected_name = '%s House of Assembly' % names[division_id]
            else:
              expected_name = 'Legislative Assembly of %s' % names[division_id]
            jurisdiction_id_suffix = 'legislature'
          elif ocd_type == 'csd':
            province_or_territory_type_id = province_and_territory_codes[ocd_type_id[:2]].split(':')[-1]
            expected_module_name = 'ca_%s_%s' % (province_or_territory_type_id, slug(division_id))
            if ocd_type_id[:2] == '24':
              expected_name = 'Conseil municipal de %s' % names[division_id]
            else:
              name_infix = census_subdivision_types[division_id]
              if name_infix in ('Municipality', 'Specialized municipality'):
                name_infix = 'Municipal'
              elif name_infix == 'Regional municipality':
                name_infix = 'Regional'
              expected_name = '%s %s Council' % (names[division_id], name_infix)
            jurisdiction_id_suffix = 'council'
          elif ocd_type == 'arrondissement':
            census_subdivision_type_id = sections[-2].split(':')[-1]
            province_or_territory_type_id = province_and_territory_codes[census_subdivision_type_id[:2]].split(':')[-1]
            expected_module_name = 'ca_%s_%s_%s' % (province_or_territory_type_id, slug('/'.join(sections[:-1])), slug(division_id))
            if names[division_id][0] in ('A', 'E', 'I', 'O', 'U'):
              expected_name = "Conseil d'arrondissement d'%s" % names[division_id]
            elif names[division_id][:3] == 'Le ':
              expected_name = "Conseil d'arrondissement du %s" % names[division_id][3:]
            else:
              expected_name = "Conseil d'arrondissement de %s" % names[division_id]
            jurisdiction_id_suffix = 'council'
          else:
            raise Exception('%s: Unrecognized OCD type %s' % (module_name, ocd_type))
          expected_jurisdiction_id = division_id.replace('ocd-division', 'ocd-jurisdiction') + '/' + jurisdiction_id_suffix

          # Determine the expected class name.
          class_name_parts = re.split('[ -]', re.sub(u"[—–]", '-', re.sub("['.]", '', names[division_id])))
          expected_class_name = unidecode(unicode(''.join(word if re.match('[A-Z]', word) else word.capitalize() for word in class_name_parts)))

          # Warn if there is no expected legislative URL.
          url = getattr(obj, 'url', None)
          expected_url = None
          if urls.get(division_id):
            expected_url = urls[division_id]
          else:
            print '%-60s %s' % (module_name, url)

          # Warn if the name may be incorrect.
          name = getattr(obj, 'name', None)
          if name != expected_name:
            print '%-60s %s' % (name, expected_name)

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

          # Set the division_name, jurisdiction_id and url appropriately.
          division_name = getattr(obj, 'division_name', None)
          expected_division_name = names[division_id]
          if division_name != expected_division_name or jurisdiction_id != expected_jurisdiction_id or (expected_url and url != expected_url):
           with codecs.open(os.path.join(module_name, '__init__.py'), 'r', 'utf8') as f:
              content = f.read()
           with codecs.open(os.path.join(module_name, '__init__.py'), 'w', 'utf8') as f:
              if division_name != expected_division_name:
                content = content.replace(division_name, expected_division_name)
              if jurisdiction_id != expected_jurisdiction_id:
                content = content.replace(jurisdiction_id, expected_jurisdiction_id)
              if expected_url and url != expected_url:
                content = content.replace(url, expected_url)
              f.write(content)

          # Name the module correctly.
          if module_name != expected_module_name:
            index.move([module_name, expected_module_name])
        else:
          print 'No OCD division for %s' % module_name
