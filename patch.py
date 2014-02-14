from copy import deepcopy
import re

from pupa.models.utils import DatetimeValidator
from pupa.models.schemas.common import links as _links, contact_details as _contact_details
from pupa.models.schemas.person import schema as person_schema
from pupa.models.schemas.membership import schema as membership_schema
from pupa.models.schemas.organization import schema as organization_schema

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
membership_links             = deepcopy(_links)
organization_contact_details = deepcopy(_contact_details)
organization_links           = deepcopy(_links)
person_contact_details       = deepcopy(_contact_details)
person_links                 = deepcopy(_links)

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
# A person should have at most one link per social media website.
person_links['maxSocialItems'] = 1
# A person should have, in most cases, at most one non-social media link.
person_links['maxNonSocialItems'] = 1

membership_schema['properties']['links']             = membership_links
organization_schema['properties']['contact_details'] = organization_contact_details
organization_schema['properties']['links']           = organization_links
person_schema['properties']['contact_details']       = person_contact_details
person_schema['properties']['links']                 = person_links


social_re = re.compile(r'(?:facebook|twitter|youtube)\.com')
social_re_list = [
  re.compile(r'facebook\.com'),
  re.compile(r'twitter\.com'),
  re.compile(r'youtube\.com'),
]

def validate_maxSocialItems(self, x, fieldname, schema, length=None):
  value = x.get(fieldname)
  for pattern in social_re_list:
    count = 0
    for link in value:
      if pattern.search(link['url']):
        count += 1
      if count > length:
        self._error("Number of items in %(value)r for field '%(fieldname)s' "
                    "with the same social media URL "
                    "must be less than or equal to %(length)d",
                    value, fieldname, length=length)

def validate_maxNonSocialItems(self, x, fieldname, schema, length=None):
  value = x.get(fieldname)
  count = 0
  for link in value:
    if not social_re.search(link['url']):
      count += 1
    if count > length:
      self._error("Number of items in %(value)r for field '%(fieldname)s' "
                  "with a non-social media URL "
                  "must be less than or equal to %(length)d",
                  value, fieldname, length=length)

DatetimeValidator.validate_maxSocialItems = validate_maxSocialItems
DatetimeValidator.validate_maxNonSocialItems = validate_maxNonSocialItems
