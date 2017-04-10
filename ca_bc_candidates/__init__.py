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
        {'name': "B.C. New Republican Party"},
        {'name': "B.C. Vision"},
        {'name': "BC Citizens First Party"},
        {'name': "BC First Party"},
        {'name': "BC Marijuana Party"},
        {'name': "BC NDP"},
        {'name': "BC Progressive Party"},
        {'name': "BC Refederation Party"},
        {'name': "British Columbia Action Party"},
        {'name': "British Columbia Conservative Party"},
        {'name': "British Columbia Excalibur Party"},
        {'name': "British Columbia Liberal Party"},
        {'name': "British Columbia Libertarian Party"},
        {'name': "British Columbia Party"},
        {'name': "British Columbia Peoples Party"},
        {'name': "British Columbia Social Credit Party"},
        {'name': "British Columbia Social Credit Party"},
        {'name': "Christian Heritage Party of British Columbia"},
        {'name': "Communist Party of BC"},
        {'name': "Cultural Action Party"},
        {'name': "For British Columbia"},
        {'name': "Green Party of British Columbia"},
        # {'name': "Green Party Political Association of British Columbia"},
        {'name': "Land Air Water Party"},
        {'name': "People's Front"},
        {'name': "The Cascadia Party of British Columbia"},
        {'name': "The Platinum Party of Employers Who Think and Act to Increase Awareness"},
        {'name': "The Vancouver Island Party"},
        {'name': "Unparty: The Consensus-Building Party"},
        {'name': "Work Less Party of British Columbia"},
        {'name': "Your Political Party of BC"},
        {'name': "Independent"},
    ]

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)

        for division in Division.get(self.division_id).children('ed'):
            if division.attrs['validFrom'] == '2017-05-09':
                organization.add_post(role='candidate', label=division.name)

        yield organization
