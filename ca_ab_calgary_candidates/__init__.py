from utils import CanadianJurisdiction
from opencivicdata.divisions import Division
from pupa.scrape import Organization


class CalgaryCandidates(CanadianJurisdiction):
    classification = 'executive'  # just to avoid clash
    division_id = 'ocd-division/country:ca/csd:4806016'
    division_name = 'Calgary'
    name = 'Calgary City Council'
    url = 'http://www.calgary.ca'

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)

        organization.add_post(role='candidate', label=self.division_name, division_id=self.division_id)
        for division in Division.get(self.division_id).children('ward'):
            organization.add_post(role='candidate', label=division.name, division_id=division.id)

        yield organization
