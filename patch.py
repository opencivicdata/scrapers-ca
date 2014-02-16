from copy import deepcopy
import re

from pupa.models.utils import DatetimeValidator
from pupa.models.schemas.common import links as _links, contact_details as _contact_details
from pupa.models.schemas.person import schema as person_schema
from pupa.models.schemas.membership import schema as membership_schema
from pupa.models.schemas.organization import schema as organization_schema

from constants import names, posts, styles

# Enumerations.
_contact_details['items']['properties']['type']['enum'] = [
  'address',
  'cell',
  'email',
  'fax',
  'voice',
]
_contact_details['items']['properties']['note']['enum'] = [
  'constituency',
  'legislature',
  'office',
  'residence',
]

# We must copy the subschema for each model.
membership_contact_details   = deepcopy(_contact_details)
membership_links             = deepcopy(_links)
organization_contact_details = deepcopy(_contact_details)
organization_links           = deepcopy(_links)
person_contact_details       = deepcopy(_contact_details)
person_links                 = deepcopy(_links)

social_re   = re.compile(r'(?:facebook|twitter|youtube)\.com')
facebook_re = re.compile(r'facebook\.com')
twitter_re  = re.compile(r'twitter\.com')
youtube_re  = re.compile(r'youtube\.com')

matchers = [
  (
    0,
    lambda x: x['type'] == 'email' and x['note'] != None,
    'Membership has email with non-empty note',
  ), (
    0,
    lambda x: x['type'] != 'email' and x['note'] == None,
    'Membership has non-email with empty note',
  ), (
    1,
    lambda x: x['type'] == 'email',
    'Membership has multiple contact_details with same type: email',
  ),
]

for type in ('address', 'cell', 'fax', 'voice'):
  for note in ('constituency', 'legislature', 'office', 'residence'):
    matchers.append((
      1,
      lambda x, type=type, note=note: x['type'] == type and x['note'] == note,
      'Membership has multiple contact_details with same type and note',
    ))

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
  (
    1,
    lambda x: not social_re.search(x['url']),
    'Person has multiple non-social media links',
  ), (
    1,
    lambda x: facebook_re.search(x['url']),
    'Person has multiple facebook.com links',
  ), (
    1,
    lambda x: twitter_re.search(x['url']),
    'Person has multiple twitter.com links',
  ), (
    1,
    lambda x: youtube_re.search(x['url']),
    'Person has multiple youtube.com links',
  ),
]

membership_schema['properties']['post_id']['post']   = True
membership_schema['properties']['role']['enum']      = lambda x: styles.get(re.sub(r'\/(?:council|legislature)\Z', '', x['organization_id'].replace('jurisdiction:ocd-jurisdiction', 'ocd-division')), ['member'])
membership_schema['properties']['contact_details']   = membership_contact_details
membership_schema['properties']['links']             = membership_links
organization_schema['properties']['contact_details'] = organization_contact_details
organization_schema['properties']['links']           = organization_links
person_schema['properties']['contact_details']       = person_contact_details
person_schema['properties']['links']                 = person_links


def validate_post(self, x, fieldname, schema, post):
  if post:
    division_id = re.sub(r'\/(?:council|legislature)\Z', '', x['organization_id'].replace('jurisdiction:ocd-jurisdiction', 'ocd-division'))
    value = x.get(fieldname)
    if posts.get(division_id):
      # Not among the known posts for the division.
      if value not in posts[division_id]:
        self._error("Post: Value %(value)r for field '%(fieldname)s' is not "
                    "in the enumeration: %(options)r",
                    value, fieldname, options=posts[division_id])
    else:
      # Not a unique role.
      if x['role'] not in uniqueRoles:
        self._error("Post: Value %(value)r for field '%(fieldname)s' is not "
                    "in the enumeration: %(options)r",
                    x['role'], 'role', options=uniqueRoles)
      # A unique role that's not among the known roles for the division.
      if styles.get(division_id) and x['role'] not in styles[division_id]:
        self._error("Post: Value %(value)r for field '%(fieldname)s' is not "
                    "in the enumeration: %(options)r",
                    x['role'], 'role', options=styles[division_id])
      # A unique role that's among the known roles for the division, but where the post doesn't match the name of the division.
      if value != names[division_id]:
        self._error("Post: Value %(value)r for field '%(fieldname)s' is not "
                    "in the enumeration: %(options)r",
                    value, fieldname, options=[names[division_id]])

DatetimeValidator.validate_post = validate_post

def validate_maxMatchingItems(self, x, fieldname, schema, tuples=None):
  value = x.get(fieldname)
  if isinstance(value, list):
    for length, method, message in tuples:
      count = 0
      for v in value:
        if method(v):
          count += 1
        if count > length:
          self._error('%s (%s)' % (message, v), value, fieldname)

DatetimeValidator.validate_maxMatchingItems = validate_maxMatchingItems
