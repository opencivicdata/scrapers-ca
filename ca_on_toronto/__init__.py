from utils import CanadianJurisdiction
from opencivicdata.divisions import Division
from pupa.scrape import Organization

from datetime import datetime


class Toronto(CanadianJurisdiction):
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
    member_role = 'Councillor'

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)

        division_names = {
            'Etobicoke North',
            'Etobicoke Centre',
            'Etobicoke-Lakeshore',
            'Parkdale-High Park',
            'York South-Weston',
            'York Centre',
            'Humber River-Black Creek',
            'Eglinton-Lawrence',
            'Davenport',
            'Spadina-Fort York',
            'University-Rosedale',
            'Toronto-St. Paul\'s',
            'Toronto Centre',
            'Toronto-Danforth',
            'Don Valley West',
            'Don Valley East',
            'Don Valley North',
            'Willowdale',
            'Beaches-East York',
            'Scarborough Southwest',
            'Scarborough Centre',
            'Scarborough-Agincourt',
            'Scarborough North',
            'Scarborough-Guildwood',
            'Scarborough-Rouge Park',
        }

        division = Division.get(self.division_id)
        organization.add_post(role='Mayor', label=division.name, division_id=division.id)

        for division in Division.get('ocd-division/country:ca/csd:3520005').children('ward'):
            if '2018' in division.id:
                organization.add_post(role='Councillor', label=division.name, division_id=division.id)

        yield organization