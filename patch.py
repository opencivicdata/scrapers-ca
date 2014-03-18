# coding: utf-8
from copy import deepcopy

import regex as re
from pupa.models.utils import DatetimeValidator
from pupa.models.schemas.common import contact_details as _contact_details, links as _links, sources as _sources
from pupa.models.schemas.person import schema as person_schema
from pupa.models.schemas.membership import schema as membership_schema
from pupa.models.schemas.organization import schema as organization_schema

from constants import names, subdivisions, styles

# @todo Test that image resolves.

_contact_details['items']['properties']['type']['blank'] = False
_contact_details['items']['properties']['type']['enum'] = [
  'address',
  'cell',
  'email',
  'fax',
  'voice',
]
_contact_details['items']['properties']['value']['blank'] = False
_contact_details['items']['properties']['value']['conditionalPattern'] = [
  (re.compile(r'\A([^@\s]+)@(?:[A-Za-z0-9-]+\.)+[A-Za-z]{2,}\Z', flags=re.U),
    lambda x: x['type'] == 'email'),
  (re.compile(r'\A1-\d{3}-\d{3}-\d{4}(?: x\d+)?\Z', flags=re.U),
    lambda x: x['type'] in ('text', 'voice', 'fax', 'cell', 'video', 'pager')),
  # Ends with a locality, a province or territory code, and an optional postal code.
  # @todo Uncomment.
  # (re.compile(r'\n(?:(?:\d+[A-C]?|St\.|a|aux|de|des|du|la|sur|\p{Lu}|(?:D'|d'|L'|l'|Mc|Qu')?\p{L}+(?:'s|!)?)(?:--?| - | ))+(?:BC|AB|MB|SK|ON|QC|NB|PE|NS|NL|YT|NT|NU)(?:  [ABCEGHJKLMNPRSTVXY][0-9][ABCEGHJKLMNPRSTVWXYZ] [0-9][ABCEGHJKLMNPRSTVWXYZ][0-9])?\Z', flags=re.U),
  #  lambda x: x['type'] == 'address'),
]
_contact_details['items']['properties']['note']['enum'] = [
  'constituency',
  'legislature',
  'office',
  'residence',
]
_contact_details['items']['additionalProperties'] = False

_links['items']['properties']['url']['blank'] = False
_links['items']['properties']['url']['compiledPattern'] = re.compile(r'\A(?:ftp|https?)://', flags=re.U)
_links['items']['additionalProperties'] = False

_sources['items']['properties']['url']['blank'] = False
_sources['items']['properties']['url']['compiledPattern'] = re.compile(r'\A(?:ftp|https?)://', flags=re.U)
_sources['items']['additionalProperties'] = False

# We must copy the subschema for each model.
membership_contact_details = deepcopy(_contact_details)
membership_links = deepcopy(_links)
organization_contact_details = deepcopy(_contact_details)
organization_links = deepcopy(_links)
person_contact_details = deepcopy(_contact_details)
person_links = deepcopy(_links)

social_re = re.compile(r'(?:facebook|twitter|youtube)\.com')
facebook_re = re.compile(r'facebook\.com')
twitter_re = re.compile(r'twitter\.com')
youtube_re = re.compile(r'youtube\.com')

matchers = [
  (0, lambda x: x['type'] == 'email' and x['note'] is not None,
    'Membership has email with non-empty note (%s)'),
  (0, lambda x: x['type'] != 'email' and x['note'] is None,
    'Membership has non-email with empty note (%s)'),
  (1, lambda x: x['type'] == 'email',
    'Membership has many emails (%s)'),
]

for type in ('address', 'cell', 'fax', 'voice'):
  for note in ('constituency', 'legislature', 'office', 'residence'):
    matchers.append((1, lambda x, type=type, note=note: x['type'] == type and x['note'] == note,
      'Membership has contact_details with same type and note (%s)'))

# A membership should not have notes on emails, should have notes on non-emails,
# should have at most one email, and should, in most cases, have at most one of
# each combination of type and note.
membership_contact_details['maxMatchingItems'] = matchers
# A membership should not have links.
membership_links['maxItems'] = 0
# An organization should not have contact details.
organization_contact_details['maxItems'] = 0
# An organization should not have links.
organization_links['maxItems'] = 0
# A person should not have contact details.
person_contact_details['maxItems'] = 0
# A person should not have notes on links.
person_links['items']['properties']['note']['type'] = 'null'
# A person should have, in most cases, at most one non-social media link, and
# should have at most one link per social media website.
person_links['maxMatchingItems'] = [
  (1, lambda x: not social_re.search(x['url']),
    'Person has many non-social media links (%s)'),
  (1, lambda x: facebook_re.search(x['url']),
    'Person has many facebook.com links (%s)'),
  (1, lambda x: twitter_re.search(x['url']),
    'Person has many twitter.com links (%s)'),
  (1, lambda x: youtube_re.search(x['url']),
    'Person has many youtube.com links (%s)'),
]

membership_schema['properties']['role']['blank'] = False
membership_schema['properties']['post_id']['post'] = True
membership_schema['properties']['role']['enum'] = lambda x: ['candidate'] + styles.get(re.sub(r'\/(?:council|legislature)\Z', '', x['organization_id'].replace('jurisdiction:ocd-jurisdiction', 'ocd-division')), ['member'])
membership_schema['properties']['contact_details'] = membership_contact_details
membership_schema['properties']['links'] = membership_links
membership_schema['matches'] = [(
  lambda x: next((True for y in x['contact_details'] if y['type'] == 'email'), False),
  lambda x: (
    x['organization_id'].startswith('party:') or
    x['organization_id'] in (
      # Javascript-encoded email
      'jurisdiction:ocd-jurisdiction/country:ca/csd:1217030/council', # Cape Breton
      # Webform email
      'jurisdiction:ocd-jurisdiction/country:ca/csd:1310032/council', # Fredericton
      'jurisdiction:ocd-jurisdiction/country:ca/csd:2423027/council', # Québec
      'jurisdiction:ocd-jurisdiction/country:ca/csd:2466097/council', # Pointe-Claire
      'jurisdiction:ocd-jurisdiction/country:ca/csd:3530016/council', # Waterloo
      'jurisdiction:ocd-jurisdiction/country:ca/csd:3530035/council', # Woolwich
      'jurisdiction:ocd-jurisdiction/country:ca/csd:4706027/council', # Regina
    ) or x['organization_id'] in (
      'jurisdiction:ocd-jurisdiction/country:ca/csd:2494068/council', # Saguenay
      'jurisdiction:ocd-jurisdiction/country:ca/csd:3520005/council', # Toronto
      'jurisdiction:ocd-jurisdiction/country:ca/csd:3521024/council', # Caledon
      'jurisdiction:ocd-jurisdiction/country:ca/csd:3530013/council', # Kitchener
    ) and x['role'] in ('Maire', 'Mayor')
  ),
  'Membership has no emails %(organization_id)s %(post_id)r',
)]

organization_schema['properties']['contact_details'] = organization_contact_details
organization_schema['properties']['links'] = organization_links

# Match initials, all-caps, short words, parenthesized nickname, and regular names.
name_fragment = r"""(?:(?:\p{Lu}\.)+|\p{Lu}+|(?:Jr|Sr|St)\.|da|de|la|van|von|\(\p{Lu}\p{Ll}*(?:-\p{Lu}\p{Ll}*)*\)|(?:D'|d'|De|de|Des|Di|Du|L'|La|Le|Mac|Mc|O'|San|Van|Vander)?\p{Lu}\p{Ll}+|Prud'homme)"""

person_schema['properties']['name']['blank'] = False
# Name components can be joined by apostrophes, hyphens or spaces.
person_schema['properties']['name']['compiledPattern'] = re.compile(r"\A(?:" + name_fragment + r"(?:'|-| - | ))*" + name_fragment + r"\Z", flags=re.U)
person_schema['properties']['name']['negativePattern'] = re.compile(r"\A(?:Councillor|Dr|Hon|M|Mayor|Miss|Mme|Mr|Mrs|Ms)\b\.?", flags=re.U)
person_schema['properties']['gender']['enum'] = ['male', 'female']
# @todo Uncomment.
# person_schema['properties']['image']['blank'] = False
person_schema['properties']['contact_details'] = person_contact_details
person_schema['properties']['links'] = person_links
# post_id is used to disambiguate people within a jurisdiction.
person_schema['properties']['post_id'] = {'type': 'string', 'blank': False}

uniqueRoles = [
  # Provincial
  'Premier',
  # Municipal
  'Acting Chief Administrative Officer',
  'Administrator',
  'Chairperson',
  'Chief Administrative Officer',
  'Chief Executive Officer',
  'City Manager',
  'Maire',
  'Mayor', 'Acting Mayor', 'Deputy Mayor', 'Interim Mayor',
  'Municipal Administrator',
  'Regional Chair',
  'Reeve', 'Deputy Reeve',
  'Warden', 'Deputy Warden',
]

def validate_post(self, x, fieldname, schema, post):
  if post and not x['organization_id'].startswith('party:'):
    division_id = re.sub(r'\/(?:council|legislature)\Z', '', x['organization_id'].replace('jurisdiction:ocd-jurisdiction', 'ocd-division'))
    value = x.get(fieldname)
    if subdivisions.get(division_id):
      # Not among the known subdivisions for the division.
      if value not in subdivisions[division_id] and not re.search(r'\AWards \d(?:(?:,| & | and )\d+)+\Z', value):
        self._error("Post: Value %(value)r for field '%(fieldname)s' is not "
                    "in the enumeration: %(options)r",
                    value, fieldname, options=subdivisions[division_id])
    else:
      # Not a unique role.
      if x['role'] not in uniqueRoles:
        self._error("Post: No known subdivisions for this division for non-unique role %(value)r",
                    x['role'], 'role', options=uniqueRoles)
      # A unique role that's not among the known roles for the division.
      if styles.get(division_id) and x['role'] not in styles[division_id]:
        self._error("Post: Unique role %(value)r is not in the enumeration: %(options)r",
                    x['role'], 'role', options=styles[division_id])
      # A unique role that's among the known roles for the division, but where the post doesn't match the name of the division.
      if names.get(division_id) and value != names[division_id]:
        self._error("Post: Unique role's post %(value)r is not in the enumeration: %(options)r",
                    value, fieldname, options=[names[division_id]])
      else:
        self._error("Post: Cannot validate unique role's post %(value)r in division %(division_id)r",
                    value, fieldname, division_id=division_id)

DatetimeValidator.validate_post = validate_post


def validate_compiledPattern(self, x, fieldname, schema, pattern=None):
  value = x.get(fieldname)
  if isinstance(value, basestring):
    if not pattern.search(value):
      self._error("Value %(value)r for field '%(fieldname)s' does "
                  "not match regular expression '%(pattern)s'",
                  value, fieldname, pattern=pattern)

DatetimeValidator.validate_compiledPattern = validate_compiledPattern


def validate_negativePattern(self, x, fieldname, schema, pattern=None):
  value = x.get(fieldname)
  if isinstance(value, basestring):
    if pattern.search(value):
      self._error("Value %(value)r for field '%(fieldname)s' "
                  "matches regular expression '%(pattern)s'",
                  value, fieldname, pattern=pattern)

DatetimeValidator.validate_negativePattern = validate_negativePattern


def validate_conditionalPattern(self, x, fieldname, schema, arguments=None):
  value = x.get(fieldname)
  if isinstance(value, basestring):
    for pattern, method in arguments:
      if method(x) and not pattern.search(value):
        self._error("Value %(value)r for field '%(fieldname)s' does "
                    "not match regular expression '%(pattern)s'",
                    value, fieldname, pattern=pattern)

DatetimeValidator.validate_conditionalPattern = validate_conditionalPattern


def validate_maxMatchingItems(self, x, fieldname, schema, arguments=None):
  value = x.get(fieldname)
  if isinstance(value, list):
    for length, method, message in arguments:
      count = 0
      for v in value:
        if method(v):
          count += 1
        if count > length:
          self._error(message % v, value, fieldname)

DatetimeValidator.validate_maxMatchingItems = validate_maxMatchingItems


def validate_matches(self, x, fieldname, schema, arguments=None):
  value = x['_data']
  for method, condition, message in arguments:
    if not condition(value) and not method(value):
      self._error(message % value, None, fieldname)

DatetimeValidator.validate_matches = validate_matches
