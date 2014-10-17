from __future__ import unicode_literals
from utils import CanadianJurisdiction


# The municipal association lists only top-level officials.
# @see http://afmnb.org/municipalite_membre.cfm?id=12
class NewBrunswickMunicipalities(CanadianJurisdiction):
    classification = 'legislature'
    division_id = 'ocd-division/country:ca/province:nb'
    division_name = 'New Brunswick'
    name = 'New Brunswick Municipalities'
    url = 'http://www2.gnb.ca/content/gnb/en/departments/elg/local_government/content/community_profiles.html'
