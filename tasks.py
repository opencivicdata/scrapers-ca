# coding: utf8

import importlib
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

# Map Standard Geographical Classification codes for provinces and territories.
reader = csv_reader('https://raw.github.com/opencivicdata/ocd-division-ids/master/mappings/country-ca-sgc/ca_provinces_and_territories.csv')
province_and_territory_abbreviations = {}
for row in reader:
  province_and_territory_abbreviations[int(row[1])] = row[0].split(':')[-1]

# Province and territory names.
reader = csv_reader('https://raw.github.com/opencivicdata/ocd-division-ids/master/identifiers/country-ca/ca_provinces_and_territories.csv')
province_and_territory_names = {}
for row in reader:
  province_and_territory_names[row[0].split(':')[-1]] = row[1]

# Census subdivision URLs.
# reader = csv_reader('https://raw.github.com/opencivicdata/ocd-division-ids/master/mappings/country-ca-urls/ca_census_subdivisions.rb') # @todo switch to .csv extension
# census_subdivision_urls = {}
# for row in reader:
#   census_subdivision_urls[int(row[0].split(':')[-1])] = row[1]

# Census subdivision type names.
census_subdivision_type_names = {}
document = lxml.html.fromstring(requests.get('http://www12.statcan.gc.ca/census-recensement/2011/ref/dict/table-tableau/table-tableau-5-eng.cfm').content)
for abbr in document.xpath('//table/tbody/tr/th[1]/abbr'):
  census_subdivision_type_names[abbr.text_content()] = re.sub(' /.+\Z', '', abbr.attrib['title'])

# Census subdivision types.
reader = csv_reader('https://raw.github.com/opencivicdata/ocd-division-ids/master/mappings/country-ca-types/ca_census_subdivisions.csv')
census_subdivision_types = {}
for row in reader:
  census_subdivision_types[int(row[0].split(':')[-1])] = census_subdivision_type_names[row[1].decode('utf-8')]

# Map Standard Geographical Classification codes for census subdivisions.
geographic_name_re = re.compile('\A([^/(]+)')
reader = csv_reader('http://www12.statcan.gc.ca/census-recensement/2011/dp-pd/hlt-fst/pd-pl/FullFile.cfm?T=301&LANG=Eng&OFT=CSV&OFN=98-310-XWE2011002-301.CSV')
reader.next()  # title
reader.next()  # headers
reader.next()  # Canada
census_subdivision_names = {}
for row in reader:
  if row:
    result = geographic_name_re.search(row[1].decode('iso-8859-1'))
    if result:
      census_subdivision_names[int(row[0])] = result.group(1).strip()
    else:
      raise Exception('Unrecognized geographic name "%s"' % row[1])
  else:
    break

repo = Repo('.')
index = repo.index

translation = {
  ord(u' '): u'_',
  ord(u"'"): u'_',
  ord(u'-'): u'_',
  ord(u'.'): None,
}

for module_name in os.listdir('.'):
  jurisdiction_ids = set()
  geographic_codes = set()

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

        geographic_code = getattr(obj, 'geographic_code', None)
        if geographic_code:
          instance = obj()

          # Ensure geographic_code is unique.
          if geographic_code in geographic_codes:
            raise Exception('Duplicate geographic_code %s' % geographic_code)
          else:
            geographic_codes.add(geographic_code)

          # Determine the expected module name, class name and jurisdiction_id.
          length = len(str(geographic_code))
          if length == 2:
            expected_class_name = province_and_territory_names[province_and_territory_abbreviations[geographic_code]]
            if geographic_code < 60:
              expected_jurisdiction_id = 'ocd-jurisdiction/country:ca/province:%s/legislature' % province_and_territory_abbreviations[geographic_code]
            else:
              expected_jurisdiction_id = 'ocd-jurisdiction/country:ca/territory:%s/legislature' % province_and_territory_abbreviations[geographic_code]
            expected_module_name = u'ca_%s' % province_and_territory_abbreviations[geographic_code]
          elif length == 7:
            expected_class_name = census_subdivision_names[geographic_code]
            expected_jurisdiction_id = 'ocd-jurisdiction/country:ca/csd:%s/council' % geographic_code
            expected_module_name = u'ca_%s_%s' % (province_and_territory_abbreviations[int(str(geographic_code)[:2])], unidecode(census_subdivision_names[geographic_code].lower().translate(translation)))
          expected_class_name = unidecode(unicode(''.join(word if re.match('[A-Z]', word) else word.capitalize() for word in re.split('[ -]', expected_class_name.replace('.', '')))))

          # legislature_url = instance.metadata['legislature_url']
          # if census_subdivision_urls.get(geographic_code):
          #   expected_legislature_url = census_subdivision_urls[geographic_code]
          # else:
          #   expected_legislature_url = None
          #   print '%s %s' % (module_name, legislature_url)

          # Warn if the legislature_name may be incorrect.
          legislature_name = instance.metadata['legislature_name']
          if str(geographic_code)[:2] == '24':
            expected_legislature_name = 'Conseil municipal de %s' % census_subdivision_names[geographic_code]
          else:
            word = census_subdivision_types[geographic_code]
            if word in ('Municipality', 'Specialized municipality'):
              word = 'Municipal'
            elif word == 'Regional municipality':
              word = 'Regional'
            expected_legislature_name = '%s %s Council' % (census_subdivision_names[geographic_code], word)
          if legislature_name != expected_legislature_name:
            print '%-50s %s' % (legislature_name, expected_legislature_name)

          # Name the class and set the jurisdiction_id correctly.
          class_name = obj.__name__
          if class_name != expected_class_name or jurisdiction_id != expected_jurisdiction_id:
            for basename in os.listdir(module_name):
              if basename.endswith('.py'):
                with open(os.path.join(module_name, basename)) as f:
                  content = f.read()
                with open(os.path.join(module_name, basename), 'w') as f:
                  if class_name != expected_class_name:
                    content = content.replace(class_name, expected_class_name)
                  if jurisdiction_id != expected_jurisdiction_id:
                    content = content.replace(jurisdiction_id, expected_jurisdiction_id)
                  f.write(content)

          # Set the name and legislature_url appropriately.
          name = instance.metadata['name']
          expected_name = census_subdivision_names[geographic_code]
          if name != expected_name or (expected_legislature_url and legislature_url != expected_legislature_url):
           with open(os.path.join(module_name, '__init__.py')) as f:
              content = f.read()
           with open(os.path.join(module_name, '__init__.py'), 'w') as f:
              if name != expected_name:
                content = content.replace(name, expected_name)
              if legislature_url != expected_legislature_url:
                content = content.replace(legislature_url, expected_legislature_url)
              f.write(content)

          # Name the module correctly.
          if module_name != expected_module_name:
            index.move([module_name, expected_module_name])
        # else:
        #   print 'No geographic_code for %s' % module_name

# @todo
# legislature_url: compare to source_url in scraped data
# assign appropriate jurisdiction_id and geographic_code to those lacking a geographic_code
# fix all the jurisdictions without geographic_code, especially the pseudo-jurisdictions
# run PEP8
