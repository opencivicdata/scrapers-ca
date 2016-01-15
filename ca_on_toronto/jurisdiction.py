from __future__ import unicode_literals
from utils import CanadianJurisdiction
from pupa.scrape import Organization
from .constants import TWO_LETTER_ORG_CODE_SCHEME


class TorontoJurisdiction(CanadianJurisdiction):
    def __init__(self):
        super(TorontoJurisdiction, self).__init__()

    def get_organizations(self):
        for obj in super(TorontoJurisdiction, self).get_organizations():
            if type(obj) == Organization and obj.name == 'Toronto City Council':
                obj.add_name('City Council')
                obj.add_identifier('CC', scheme=TWO_LETTER_ORG_CODE_SCHEME)
            yield obj
