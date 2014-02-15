# coding: utf-8
import csv
from ftplib import FTP
import re
from StringIO import StringIO
from urlparse import urlparse

import lxml.html
import requests
from scrapelib import urlopen
from pupa.scrape import Scraper, Jurisdiction, Legislator
from pupa.models import Membership, Person

import patch

CONTACT_DETAIL_TYPE_MAP = {
  'Address': 'address',
  'bb': 'cell',
  'bus': 'voice',
  'Bus': 'voice',
  'Bus.': 'voice',
  'Business': 'voice',
  'Cell': 'cell',
  'Cell Phone': 'cell',
  'Email': 'email',
  'Fax': 'fax',
  'Home': 'voice',
  'Home Phone': 'voice',
  'Home Phone*': 'voice',
  'Office': 'voice',
  'ph': 'voice',
  u'ph\xc2': 'voice',
  'Phone': 'voice',
  'Res': 'voice',
  'Res/Bus': 'voice',
  'Residence': 'voice',
  'Voice Mail': 'voice',
  'Work': 'voice',
}
# In Newmarket, for example, there are both "Phone" and "Business" numbers.
CONTACT_DETAIL_NOTE_MAP = {
  'Address': 'legislature',
  'bb': 'legislature',
  'bus': 'office',
  'Bus': 'office',
  'Bus.': 'office',
  'Business': 'office',
  'Cell': 'legislature',
  'Cell Phone': 'legislature',
  'Email': None,
  'Fax': 'legislature',
  'Home': 'residence',
  'Home Phone': 'residence',
  'Home Phone*': 'residence',
  'ph': 'legislature',
  u'ph\xc2': 'legislature',
  'Phone': 'legislature',
  'Office': 'legislature',
  'Res': 'residence',
  'Res/Bus': 'office',
  'Residence': 'residence',
  'Voice Mail': 'legislature',
  'Work': 'legislature',
}


class CanadianJurisdiction(Jurisdiction):
  session_details = {
    'N/A': {
      '_scraped_name': 'N/A',
    }
  }
  terms = [
    {
      'name': 'N/A',
      'sessions': ['N/A'],
      'start_year': 1900,
      'end_year': 2030,
    }
  ]

  def __init__(self):
    for scraper_type in ('bills', 'events', 'people', 'speeches', 'votes'):
      try:
        __import__(self.__module__ + '.' + scraper_type)
      except ImportError:
        pass
      else:
        self.provides.append(scraper_type)

  def get_scraper(self, term, session, scraper_type):
    if scraper_type in self.provides:
      class_name = self.__class__.__name__ + {
        'bills': 'Bill',
        'events': 'Event',
        'people': 'Person',
        'speeches': 'Speech',
        'votes': 'Vote',
      }[scraper_type] + 'Scraper'
      return getattr(__import__(self.__module__ + '.' + scraper_type, fromlist=[class_name]), class_name)

  def scrape_session_list(self):
    return ['N/A']


class CanadianLegislator(Legislator):
  def __init__(self, name, post_id, **kwargs):
    super(CanadianLegislator, self).__init__(clean_name(name), clean_string(post_id), **kwargs)

  # @todo clean_string all the slots and contact detail values
  def add_link(self, url, note=None):
      if url.startswith('www.'):
        url = 'http://%s' % url
      if re.match(r'\A@[A-Za-z]+\Z', url):
        url = 'https://twitter.com/%s' % url[1:]
      self.links.append({"note": note, "url": url})

  def add_contact(self, type, value, note):
    if type in CONTACT_DETAIL_TYPE_MAP:
      type = CONTACT_DETAIL_TYPE_MAP[type]
    if note in CONTACT_DETAIL_NOTE_MAP:
      note = CONTACT_DETAIL_NOTE_MAP[note]
    if type in ('text', 'voice', 'fax', 'cell', 'video', 'pager'):
      value = clean_telephone_number(value)
    elif type == 'address':
      value = clean_address(value)
    self._contact_details.append({'type': type, 'value': value, 'note': note})


# Removes _is_legislator flag and _contact_details. Used by aggregations.
# @see https://github.com/opencivicdata/pupa/blob/master/pupa/scrape/helpers.py
class AggregationLegislator(Person):
  __slots__ = ('post_id', 'party', 'chamber')

  def __init__(self, name, post_id, party=None, chamber=None, **kwargs):
    super(AggregationLegislator, self).__init__(clean_name(name), **kwargs)
    self.post_id = clean_string(post_id)
    self.party = party
    self.chamber = chamber


whitespace_re = re.compile(r'[^\S\n]+', flags=re.U)
honorific_prefix_re = re.compile(r'\A(?:Councillor|Dr|Hon|M|Mayor|Mme|Mr|Mrs|Ms|Miss)\b\.? ')

table = {
  ord(u'​'): u' ', # zero-width space
  ord(u'’'): u"'",
}

# @see https://github.com/opencivicdata/ocd-division-ids/blob/master/identifiers/country-ca/ca_provinces_and_territories.csv
# @see https://github.com/opencivicdata/ocd-division-ids/blob/master/mappings/country-ca-fr/ca_provinces_and_territories.csv
abbreviations = {
  u'Newfoundland and Labrador': 'NL',
  u'Prince Edward Island': 'PE',
  u'Nova Scotia': 'NS',
  u'New Brunswick': 'NB',
  u'Québec': 'QC',
  u'Ontario': 'ON',
  u'Manitoba': 'MB',
  u'Saskatchewan': 'SK',
  u'Alberta': 'AB',
  u'British Columbia': 'BC',
  u'Yukon': 'YT',
  u'Northwest Territories': 'NT',
  u'Nunavut': 'NU',

  u'PEI': 'PE',
}

def clean_string(s):
  return re.sub(r' *\n *', '\n', whitespace_re.sub(' ', unicode(s).translate(table)).strip())

def clean_name(s):
  return honorific_prefix_re.sub('', clean_string(s))

# @see http://www.noslangues-ourlanguages.gc.ca/bien-well/fra-eng/typographie-typography/telephone-eng.html
def clean_telephone_number(s):
  splits = re.split(r'[\s-](?:x|ext\.?|poste)[\s-]?(?=\b|\d)', s, flags=re.IGNORECASE)
  digits = re.sub(r'\D', '', splits[0])

  if len(digits) == 10:
    digits = '1' + digits

  if len(digits) == 11 and digits[0] == '1' and len(splits) <= 2:
    digits = re.sub(r'\A(\d)(\d{3})(\d{3})(\d{4})\Z', r'\1-\2-\3-\4', digits)
    if len(splits) == 2:
      return '%s x%s' % (digits, splits[1])
    else:
      return digits
  else:
    return s

# Corrects the postal code, abbreviates the province or territory name, and
# formats the last line of the address.
def clean_address(s):
  # The letter "O" instead of the numeral "0" is a common mistake.
  s = re.sub(r'\b[A-Z][O0-9][A-Z]\s?[O0-9][A-Z][O0-9]\b', lambda x: x.group(0).replace('O', '0'), s)
  for k, v in abbreviations.iteritems():
      s = re.sub(r'[,\n ]+\(?' + k + r'\)?(?=(?:[,\n ]+Canada)?(?:[,\n ]+[A-Z][0-9][A-Z]\s?[0-9][A-Z][0-9])?\Z)', ' ' + v, s)
  return re.sub(r'[,\n ]+([A-Z]{2})(?:[,\n ]+Canada)?[,\n ]+([A-Z][0-9][A-Z])\s?([0-9][A-Z][0-9])\Z', r' \1  \2 \3', s)

def lxmlize(url, encoding='utf-8'):
  entry = urlopen(url).encode(encoding)
  page = lxml.html.fromstring(entry)
  meta = page.xpath('//meta[@http-equiv="refresh"]')
  if meta:
    _, url = meta[0].attrib['content'].split('=', 1)
    return lxmlize(url, encoding)
  else:
    page.make_links_absolute(url)
    return page

def csv_reader(url, headers=False):
  result = urlparse(url)
  if result.scheme == 'ftp':
    data = StringIO()
    ftp = FTP(result.hostname)
    ftp.login(result.username, result.password)
    ftp.retrbinary('RETR %s' % result.path, lambda block: data.write(block))
    ftp.quit()
    data.seek(0)
  else:
    data = StringIO(requests.get(url).content)
  if headers:
    return csv.DictReader(data)
  else:
    return csv.reader(data)
