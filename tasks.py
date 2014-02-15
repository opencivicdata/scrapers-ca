# coding: utf8

import importlib
import codecs
import csv
import os
import os.path
import re
import string
from StringIO import StringIO

from git import Repo
from invoke import run, task
import lxml.html
import requests
from unidecode import unidecode


# Map Standard Geographical Classification codes to the OCD identifiers of provinces and territories.
province_and_territory_codes_memo = {}
def province_and_territory_codes():
  if not province_and_territory_codes_memo:
    reader = csv_reader('https://raw.github.com/opencivicdata/ocd-division-ids/master/mappings/country-ca-sgc/ca_provinces_and_territories.csv')
    for row in reader:
      province_and_territory_codes_memo[row[1]] = row[0]
  return province_and_territory_codes_memo

# Reads a remote CSV file.
def csv_reader(url):
  return csv.reader(StringIO(requests.get(url).content))

def slug(name):
  return unidecode(unicode(name).lower().translate({
    ord(u' '): u'_',
    ord(u"'"): u'_',
    ord(u'-'): u'_',  # dash
    ord(u'—'): u'_',  # m-dash
    ord(u'–'): u'_',  # n-dash
    ord(u'.'): None,
  }))

urls_memo = {}
census_division_types = {}
census_subdivision_types = {}
names = {}
def get_definition(division_id, aggregation=False):
  if not urls_memo:
    # Map OCD identifiers to URLs.
    reader = csv_reader('https://raw.github.com/opencivicdata/ocd-division-ids/master/mappings/country-ca-urls/ca_census_subdivisions.csv')
    for row in reader:
      urls_memo[row[0].decode('utf8')] = row[1]
    reader = csv_reader('https://raw.github.com/opencivicdata/ocd-division-ids/master/mappings/country-ca-urls/census_subdivision-montreal-arrondissements.csv')
    for row in reader:
      urls_memo[row[0].decode('utf8')] = row[1]

  if not census_division_types:
    # Map census division type codes to names.
    census_division_type_names = {}
    document = lxml.html.fromstring(requests.get('http://www12.statcan.gc.ca/census-recensement/2011/ref/dict/table-tableau/table-tableau-4-eng.cfm').content)
    for abbr in document.xpath('//table/tbody/tr/th[1]/abbr'):
      census_division_type_names[abbr.text_content()] = re.sub(' /.+\Z', '', abbr.attrib['title'])

    # Map OCD identifiers to census division types.
    reader = csv_reader('https://raw.github.com/opencivicdata/ocd-division-ids/master/mappings/country-ca-types/ca_census_divisions.csv')
    for row in reader:
      census_division_types[row[0]] = census_division_type_names[row[1].decode('utf8')]

  if not census_subdivision_types:
    # Map census subdivision type codes to names.
    census_subdivision_type_names = {}
    document = lxml.html.fromstring(requests.get('http://www12.statcan.gc.ca/census-recensement/2011/ref/dict/table-tableau/table-tableau-5-eng.cfm').content)
    for abbr in document.xpath('//table/tbody/tr/th[1]/abbr'):
      census_subdivision_type_names[abbr.text_content()] = re.sub(' /.+\Z', '', abbr.attrib['title'])

    # Map OCD identifiers to census subdivision types.
    reader = csv_reader('https://raw.github.com/opencivicdata/ocd-division-ids/master/mappings/country-ca-types/ca_census_subdivisions.csv')
    for row in reader:
      census_subdivision_types[row[0]] = census_subdivision_type_names[row[1].decode('utf8')]

  # Map OCD identifiers and Standard Geographical Classification codes to names.
  if not names:
    reader = csv_reader('https://raw.github.com/opencivicdata/ocd-division-ids/master/identifiers/country-ca/census_subdivision-montreal-arrondissements.csv')
    for row in reader:
      names[row[0].decode('utf8')] = row[1].decode('utf8')
    reader = csv_reader('https://raw.github.com/opencivicdata/ocd-division-ids/master/identifiers/country-ca/ca_provinces_and_territories.csv')
    for row in reader:
      names[row[0].decode('utf8')] = row[1].decode('utf8')
    reader = csv_reader('https://raw.github.com/opencivicdata/ocd-division-ids/master/identifiers/country-ca/ca_census_divisions.csv')
    for row in reader:
      names[row[0].decode('utf8')] = row[1].decode('utf8')
    reader = csv_reader('https://raw.github.com/opencivicdata/ocd-division-ids/master/identifiers/country-ca/ca_census_subdivisions.csv')
    for row in reader:
      names[row[0].decode('utf8')] = row[1].decode('utf8')

  codes = province_and_territory_codes()

  expected = {}

  sections = division_id.split('/')
  ocd_type, ocd_type_id = sections[-1].split(':')

  # Determine the module name, name and jurisdiction_id.
  if ocd_type in ('province', 'territory'):
    pattern = 'ca_%s_municipalities' if aggregation else 'ca_%s'
    expected['module_name'] = pattern % ocd_type_id
    if aggregation:
      expected['name'] = '%s Municipalities' % names[division_id]
    elif ocd_type_id in ('nl', 'ns'):
      expected['name'] = '%s House of Assembly' % names[division_id]
    else:
      expected['name'] = 'Legislative Assembly of %s' % names[division_id]
    jurisdiction_id_suffix = 'municipalities' if aggregation else 'legislature'
  elif ocd_type == 'cd':
    province_or_territory_type_id = codes[ocd_type_id[:2]].split(':')[-1]
    expected['module_name'] = 'ca_%s_%s' % (province_or_territory_type_id, slug(names[division_id]))
    name_infix = census_division_types[division_id]
    if name_infix == 'Regional municipality':
      name_infix = 'Regional'
    expected['name'] = '%s %s Council' % (names[division_id], name_infix)
    expected['geographic_code'] = ocd_type_id
    jurisdiction_id_suffix = 'council'
  elif ocd_type == 'csd':
    province_or_territory_type_id = codes[ocd_type_id[:2]].split(':')[-1]
    expected['module_name'] = 'ca_%s_%s' % (province_or_territory_type_id, slug(names[division_id]))
    if ocd_type_id[:2] == '24':
      expected['name'] = 'Conseil municipal de %s' % names[division_id]
    else:
      name_infix = census_subdivision_types[division_id]
      if name_infix in ('Municipality', 'Specialized municipality'):
        name_infix = 'Municipal'
      elif name_infix == 'Regional municipality':
        name_infix = 'Regional'
      expected['name'] = '%s %s Council' % (names[division_id], name_infix)
    expected['geographic_code'] = ocd_type_id
    jurisdiction_id_suffix = 'council'
  elif ocd_type == 'arrondissement':
    census_subdivision_type_id = sections[-2].split(':')[-1]
    province_or_territory_type_id = province_and_territory_codes[census_subdivision_type_id[:2]].split(':')[-1]
    expected['module_name'] = 'ca_%s_%s_%s' % (province_or_territory_type_id, slug(names['/'.join(sections[:-1])]), slug(names[division_id]))
    if names[division_id][0] in ('A', 'E', 'I', 'O', 'U'):
      expected['name'] = "Conseil d'arrondissement d'%s" % names[division_id]
    elif names[division_id][:3] == 'Le ':
      expected['name'] = "Conseil d'arrondissement du %s" % names[division_id][3:]
    else:
      expected['name'] = "Conseil d'arrondissement de %s" % names[division_id]
    jurisdiction_id_suffix = 'council'
  else:
    raise Exception('%s: Unrecognized OCD type %s' % (module_name, ocd_type))
  expected['jurisdiction_id'] = division_id.replace('ocd-division', 'ocd-jurisdiction') + '/' + jurisdiction_id_suffix

  # Determine the class name.
  class_name_parts = re.split('[ -]', re.sub(u"[—–]", '-', re.sub("['.]", '', names[division_id])))
  expected['class_name'] = unidecode(unicode(''.join(word if re.match('[A-Z]', word) else word.capitalize() for word in class_name_parts)))
  if aggregation:
    expected['class_name'] += 'Municipalities'

  # Determine the url.
  expected['url'] = None
  if urls_memo.get(division_id):
    expected['url'] = urls_memo[division_id]

  # Determine the division name.
  expected['division_name'] = names[division_id]

  return expected

@task
def urls():
  for module_name in os.listdir('.'):
    if os.path.isdir(module_name) and module_name not in ('.git', 'scrape_cache', 'scraped_data'):
      module = importlib.import_module('%s.people' % module_name)
      print '%-60s %s' % (module_name, module.__dict__['COUNCIL_PAGE'])

@task
def new(division_id):
  expected = get_definition(division_id)
  module_name = expected['module_name']
  run('mkdir -p %s' % module_name, echo=True)

  with codecs.open(os.path.join(module_name, '__init__.py'), 'w', 'utf8') as f:
    if expected['url']:
      f.write("""# coding: utf-8
from utils import CanadianJurisdiction

class %(class_name)s(CanadianJurisdiction):
  jurisdiction_id = u'%(jurisdiction_id)s'
  geographic_code = %(geographic_code)s
  division_name = u'%(division_name)s'
  name = u'%(name)s'
  url = '%(url)s'
""" % expected)
    else:
      f.write("""# coding: utf-8
from utils import CanadianJurisdiction

class %(class_name)s(CanadianJurisdiction):
  jurisdiction_id = u'%(jurisdiction_id)s'
  geographic_code = %(geographic_code)s
  division_name = u'%(division_name)s'
  name = u'%(name)s'
""" % expected)

  with codecs.open(os.path.join(module_name, 'people.py'), 'w', 'utf8') as f:
    f.write("""# coding: utf-8
from pupa.scrape import Scraper

from utils import lxmlize, CanadianLegislator as Legislator

import re

COUNCIL_PAGE = ''

class %(class_name)sPersonScraper(Scraper):

  def get_people(self):
    pass
""" % expected)

@task
def tidy():
  repo = Repo('.')
  index = repo.index

  # Map OCD identifiers to styles of address.
  leader_styles = {}
  member_styles = {}
  reader = csv_reader('https://docs.google.com/spreadsheet/pub?key=0AtzgYYy0ZABtdFJrVTdaV1h5XzRpTkxBdVROX3FNelE&single=true&gid=0&output=csv')
  reader.next()
  for row in reader:
    key = row[0].decode('utf-8')
    leader_styles[key] = row[2].decode('utf8')
    member_styles[key] = row[3].decode('utf8')
  reader = csv_reader('https://docs.google.com/spreadsheet/pub?key=0AtzgYYy0ZABtdFJrVTdaV1h5XzRpTkxBdVROX3FNelE&single=true&gid=1&output=csv')
  reader.next()
  for row in reader:
    key = row[0].decode('utf-8')
    leader_styles[key] = row[2].decode('utf8')
    member_styles[key] = row[3].decode('utf8')

  codes = province_and_territory_codes()

  for module_name in os.listdir('.'):
    jurisdiction_ids = set()
    aggregation_division_ids = set()
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
                division_id = codes[geographic_code]
              elif length == 4:
                division_id = 'ocd-division/country:ca/cd:%s' % geographic_code
              elif length == 7:
                division_id = 'ocd-division/country:ca/csd:%s' % geographic_code
              else:
                raise Exception('%s: Unrecognized geographic code %s' % (module_name, geographic_code))

          if division_id:
            aggregation = bool(module_name.endswith('_municipalities'))

            # Ensure division_id is unique.
            if aggregation:
              if division_id in aggregation_division_ids:
                raise Exception('%s: Duplicate division_id %s' % (module_name, division_id))
              else:
                aggregation_division_ids.add(division_id)
            else:
              if division_id in division_ids:
                raise Exception('%s: Duplicate division_id %s' % (module_name, division_id))
              else:
                division_ids.add(division_id)

            expected = get_definition(division_id, aggregation)

            class_name    = obj.__name__
            division_name = getattr(obj, 'division_name', None)
            name          = getattr(obj, 'name', None)
            url           = getattr(obj, 'url', None)

            # Ensure presence of url and styles of address.
            if not member_styles.get(division_id):
              print '%-60s No member style of address: %s' % (module_name, division_id)
            if not leader_styles.get(division_id):
              print '%-60s No leader style of address: %s' % (module_name, division_id)
            if url and not expected['url']:
              print '%-60s %s' % (module_name, url)

            # Warn if the name may be incorrect.
            if name != expected['name']:
              print '%-60s %s' % (name, expected['name'])

            # Name the classes correctly.
            if class_name != expected['class_name']:
              # @note This for-loop will only run if the class name in __init__.py is incorrect.
              for basename in os.listdir(module_name):
                if basename.endswith('.py'):
                  with codecs.open(os.path.join(module_name, basename), 'r', 'utf8') as f:
                    content = f.read()
                  with codecs.open(os.path.join(module_name, basename), 'w', 'utf8') as f:
                    content = content.replace(class_name, expected['class_name'])
                    f.write(content)

            # Set the jurisdiction_id, division_name and url appropriately.
            if jurisdiction_id != expected['jurisdiction_id'] or division_name != expected['division_name'] or (expected['url'] and url != expected['url']):
             with codecs.open(os.path.join(module_name, '__init__.py'), 'r', 'utf8') as f:
                content = f.read()
             with codecs.open(os.path.join(module_name, '__init__.py'), 'w', 'utf8') as f:
                if jurisdiction_id != expected['jurisdiction_id']:
                  content = content.replace(jurisdiction_id, expected['jurisdiction_id'])
                if division_name != expected['division_name']:
                  content = content.replace(division_name, expected['division_name'])
                if expected['url'] and url != expected['url']:
                  content = content.replace(url, expected['url'])
                f.write(content)

            # Name the module correctly.
            if module_name != expected['module_name']:
              index.move([module_name, expected['module_name']])
          else:
            print 'No OCD division for %s' % module_name
