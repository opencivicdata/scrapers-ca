# coding: utf-8
from __future__ import unicode_literals

import re
from copy import deepcopy

from pupa.utils import DatetimeValidator
from pupa.scrape.schemas.common import contact_details as _contact_details, links as _links, sources as _sources
from pupa.scrape.schemas.person import schema as person_schema
from pupa.scrape.schemas.membership import schema as membership_schema
from pupa.scrape.schemas.organization import schema as organization_schema
from six import string_types

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
    (r'\A([^@\s]+)@(?:[A-Za-z0-9-]+\.)+[A-Za-z]{2,}\Z',
     lambda x: x['type'] == 'email'),
    (r'\A1-\d{3}-\d{3}-\d{4}(?: x\d+)?\Z',
        lambda x: x['type'] in ('text', 'voice', 'fax', 'cell', 'video', 'pager')),
    # Ends with a locality, a province or territory code, and an optional postal code.
    # @note We realistically will never uncomment this, as addresses are not important.
    # (re.compile(r'\n(?:(?:\d+[A-C]?|St\.|a|aux|de|des|du|la|sur|\p{Lu}|(?:D'|d'|L'|l'|Mc|Qu')?\p{L}+(?:'s|!)?)(?:--?| - | ))+(?:BC|AB|MB|SK|ON|QC|NB|PE|NS|NL|YT|NT|NU)(?:  [ABCEGHJKLMNPRSTVXY][0-9][ABCEGHJKLMNPRSTVWXYZ] [0-9][ABCEGHJKLMNPRSTVWXYZ][0-9])?\Z', flags=re.U),
    #  lambda x: x['type'] == 'address'),
]
_contact_details['items']['properties']['note']['pattern'] = r'\A(?:constituency|legislature|office|residence|)(?: \(\d\))?\Z'

_contact_details['items']['additionalProperties'] = False

_links['items']['properties']['url']['blank'] = False
_links['items']['properties']['url']['pattern'] = r'\A(?:ftp|https?)://'
_links['items']['additionalProperties'] = False

_sources['items']['properties']['url']['blank'] = False
_sources['items']['properties']['url']['pattern'] = r'\A(?:ftp|https?)://'
_sources['items']['additionalProperties'] = False

# We must copy the subschema for each model.
membership_contact_details = deepcopy(_contact_details)
membership_links = deepcopy(_links)
organization_contact_details = deepcopy(_contact_details)
organization_links = deepcopy(_links)
person_contact_details = deepcopy(_contact_details)
person_links = deepcopy(_links)

social_re = re.compile(r'(?:facebook|linkedin|twitter|youtube)\.com')
facebook_re = re.compile(r'facebook\.com')
linkedin_re = re.compile(r'linkedin\.com')
twitter_re = re.compile(r'twitter\.com')
youtube_re = re.compile(r'youtube\.com')

matchers = [
    (0, lambda x: x['type'] == 'email' and x['note'] != '',
     'Membership has email with non-empty note'),
    (0, lambda x: x['type'] != 'email' and x['note'] == '',
        'Membership has non-email with empty note'),
    (1, lambda x: x['type'] == 'email',
        'Membership has many emails'),
]

for type in ('address', 'cell', 'fax', 'voice'):
    for note in ('constituency', 'legislature', 'office', 'residence'):
        matchers.append((1, lambda x, type=type, note=note: x['type'] == type and x['note'] == note,
                         'Membership has contact_details with same type and note'))

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
person_links['items']['properties']['note']['enum'] = ['']
# A person should have, in most cases, at most one non-social media link, and
# should have at most one link per social media website.
person_links['maxMatchingItems'] = [
    (1, lambda x: not social_re.search(x['url']),
     'Person has many non-social media links'),
    (1, lambda x: facebook_re.search(x['url']),
        'Person has many facebook.com links'),
    (1, lambda x: linkedin_re.search(x['url']),
        'Person has many linkedin.com links'),
    (1, lambda x: twitter_re.search(x['url']),
        'Person has many twitter.com links'),
    (1, lambda x: youtube_re.search(x['url']),
        'Person has many youtube.com links'),
]

membership_schema['properties']['role']['blank'] = False
membership_schema['properties']['contact_details'] = membership_contact_details
membership_schema['properties']['links'] = membership_links

organization_schema['properties']['contact_details'] = organization_contact_details
organization_schema['properties']['links'] = organization_links

# Match initials, all-caps, short words, parenthesized nickname, and regular names.
name_fragment = r"""(?:(?:\p{Lu}\.)+|\p{Lu}+|(?:Jr|Sr|St)\.|da|de|la|van|von|\(\p{Lu}\p{Ll}*(?:-\p{Lu}\p{Ll}*)*\)|(?:D'|d'|De|de|Des|Di|Du|L'|La|Le|Mac|Mc|O'|San|Van|Vander)?\p{Lu}\p{Ll}+|Prud'homme)"""

# Name components can be joined by apostrophes, hyphens or spaces.
person_schema['properties']['name']['pattern'] = r'\A(?:' + name_fragment + r"(?:'|-| - | ))*" + name_fragment + r'\Z'
person_schema['properties']['name']['pattern'] = r'\A(?!(?:Chair|Councillor|Deputy|Dr|Hon|M|Mayor|Miss|Mme|Mr|Mrs|Ms|Regional|Warden)\b)'
person_schema['properties']['gender']['enum'] = ['male', 'female', '']
# @note https://github.com/opennorth/represent-canada-images checks whether an
# image resolves. Testing URLs here would slow down scraping.
person_schema['properties']['contact_details'] = person_contact_details
person_schema['properties']['links'] = person_links
# district is used to disambiguate people within a jurisdiction.
person_schema['properties']['district'] = {'type': 'string', 'blank': False}

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


def validate_conditionalPattern(self, x, fieldname, schema, path, arguments=None):
    value = x.get(fieldname)
    if isinstance(value, string_types):
        for pattern, method in arguments:
            if method(x) and not re.search(pattern, value):
                self._error("does not match regular expression '{pattern}'",
                            value, fieldname, pattern=pattern)

DatetimeValidator.validate_conditionalPattern = validate_conditionalPattern


def validate_maxMatchingItems(self, x, fieldname, schema, path, arguments=None):
    value = x.get(fieldname)
    if isinstance(value, list):
        for length, method, message in arguments:
            count = 0
            for v in value:
                if method(v):
                    count += 1
                if count > length:
                    self._error(message, value, fieldname)

DatetimeValidator.validate_maxMatchingItems = validate_maxMatchingItems
