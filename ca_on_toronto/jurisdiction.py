from __future__ import unicode_literals
from utils import CanadianJurisdiction
from pupa.scrape import Organization, Post
from opencivicdata.divisions import Division
import re
from .constants import TWO_LETTER_ORG_CODE_SCHEME, CANONICAL_COUNCIL_NAME


class TorontoJurisdiction(CanadianJurisdiction):
    def __init__(self):
        super(TorontoJurisdiction, self).__init__()

    def get_organizations(self):
        def is_council_org(obj):
            return type(obj) == Organization and obj.name == CANONICAL_COUNCIL_NAME

        for obj in super(TorontoJurisdiction, self).get_organizations():
            if is_council_org(obj):
                obj.add_name('City Council')
                obj.add_identifier('CC', scheme=TWO_LETTER_ORG_CODE_SCHEME)

            if type(obj) == Post:
                division = Division.get(obj.division_id)
                if division._type == 'ward':
                    name, number = re.match(r'(.+) \((.+)\)', division.name).groups()
                    obj.extras = {
                        'ward': {
                            'name': name,
                            'number': number,
                            }
                        }

            yield obj
