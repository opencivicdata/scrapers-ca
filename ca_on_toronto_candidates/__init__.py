from utils import CanadianJurisdiction
from opencivicdata.divisions import Division
from pupa.scrape import Organization

from datetime import datetime


class TorontoCandidates(CanadianJurisdiction):
    classification = 'executive'  # just to avoid clash
    division_id = 'ocd-division/country:ca/csd:3520005'
    division_name = 'Toronto'
    name = 'Toronto City Council'
    url = 'http://www.toronto.ca'
    parties = [
        {'name': "Alliance Party of Ontario"},
        {'name': "Cultural Action Party of Ontario"},
        {'name': "Canadians' Choice Party"},
        {'name': "Communist Party of Canada (Ontario)"},
        {'name': "Equal Parenting Party"},
        {'name': "Freedom Party of Ontario"},
        {'name': "Green Party of Ontario"},
        {'name': "New Democratic Party of Ontario"},
        {'name': "None of the Above Direct Democracy Party"},
        {'name': "Northern Ontario Party"},
        {'name': "Ontario Liberal Party"},
        {'name': "Ontario Libretarian Party"},
        {'name': "Ontario Moderate Party"},
        {'name': "Ontario Provincial Confederation of Regions Party"},
        {'name': "Party for People with Special Needs"},
        {'name': "Pauper Party of Ontario"},
        {'name': "Progressive Conservative Party of Ontario"},
        {'name': "Stop the New Sex-Ed Agenda"},
        {'name': "The Peoples Political Party"},
        {'name': "Trillium Party of Ontario"},
        {'name': "Vegan Environmental Party"},
        {'name': "Independent"},
    ]
    skip_null_valid_from = True
    valid_from = '2018-09-19'
    member_role = 'candidate'

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)

        division_names = {
            'Beaches—East York',
            'Davenport',
            'Don Valley East',
            'Don Valley North',
            'Don Valley West',
            'Eglinton—Lawrence',
            'Etobicoke Centre',
            'Etobicoke North',
            'Etobicoke—Lakeshore',
            'Humber River—Black Creek',
            'Parkdale—High Park',
            'Scarborough Centre',
            'Scarborough North',
            'Scarborough Southwest',
            'Scarborough—Agincourt',
            'Scarborough—Guildwood',
            'Scarborough—Rouge Park',
            'Spadina—Fort York',
            'Toronto Centre',
            'Toronto—Danforth',
            'Toronto—St. Paul\'s',
            'University—Rosedale',
            'Willowdale',
            'York Centre',
            'York South—Weston',
        }

        division = Division.get(self.division_id)
        organization.add_post(role='candidate', label=division.name, division_id=division.id)

        for division in Division.get('ocd-division/country:ca/province:on').children('ed'):
            if not self.skip_null_valid_from and not division.attrs.get('validFrom') or division.attrs.get('validFrom') and (division.attrs['validFrom'] <= datetime.now().strftime('%Y-%m-%d') or division.attrs['validFrom'] == self.valid_from):
                if division.name in division_names:
                    organization.add_post(role='candidate', label=division.name, division_id=division.id)

        yield organization
