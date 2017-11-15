from utils import CanadianJurisdiction
from opencivicdata.divisions import Division
from pupa.scrape import Organization

from datetime import datetime


class BritishColumbia(CanadianJurisdiction):
    classification = 'legislature'
    division_id = 'ocd-division/country:ca/province:bc'
    division_name = 'British Columbia'
    name = 'Legislative Assembly of British Columbia'
    url = 'http://www.leg.bc.ca'
    parties = [
        {'name': 'New Democratic Party of British Columbia'},
        {'name': 'British Columbia Liberal Party'},
        {'name': 'BC Green Party'},
        {'name': 'Independent'},
    ]

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)

        for division in Division.get(self.division_id).children('ed'):
            if division.attrs.get('validFrom') and division.attrs['validFrom'] <= datetime.now().strftime('%Y-%m-%d'):
                organization.add_post(role='MLA', label=division.name, division_id=division.id)

        yield organization
