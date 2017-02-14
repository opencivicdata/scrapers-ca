from utils import CanadianJurisdiction
from opencivicdata.divisions import Division
from pupa.scrape import Organization


class BritishColumbiaCandidates(CanadianJurisdiction):
    classification = 'executive'  # just to avoid clash
    division_id = 'ocd-division/country:ca/province:bc'
    division_name = 'British Columbia'
    name = 'Legislative Assembly of British Columbia'
    url = 'http://www.leg.bc.ca'
    parties = [
        {'name': 'British Columbia Liberal Party'},
        {'name': 'New Democratic Party of British Columbia'},
        {'name': 'Green Party of British Columbia'},
        {'name': 'British Columbia Conservatives'},
        {'name': 'Independent'},
    ]

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)

        for division in Division.get(self.division_id).children('ed'):
            if division.attrs['validFrom'] == '2017-05-09':
                organization.add_post(role='candidate', label=division.name)

        yield organization
