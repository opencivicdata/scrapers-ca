from utils import CanadianJurisdiction
from pupa.scrape import Organization


class NewBrunswickMunicipalities(CanadianJurisdiction):
    classification = 'legislature'
    division_id = 'ocd-division/country:ca/province:nb'
    division_name = 'New Brunswick'
    name = 'New Brunswick Municipalities'
    url = 'http://www2.gnb.ca/content/gnb/en/departments/elg/local_government/content/community_profiles.html'

    def get_organizations(self):
        return []
