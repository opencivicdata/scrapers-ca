from .jurisdiction import TorontoJurisdiction
from opencivicdata.divisions import Division
from pupa.scrape import Organization

import lxml.html
import requests


class Toronto(TorontoJurisdiction):
    classification = 'legislature'
    division_id = 'ocd-division/country:ca/csd:3520005'
    division_name = 'Toronto'
    name = 'Toronto City Council'
    url = 'http://www.toronto.ca'
    legislative_sessions = []

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)

        organization.add_post(role='Mayor', label=self.division_name, division_id=self.division_id)
        for division in Division.get('ocd-division/country:ca/csd:3520005').children('ward'):
            if '2018' in division.id:
                organization.add_post(role='Councillor', label=division.name, division_id=division.id)

        yield organization

    def __init__(self):
        super().__init__()
        self.legislative_sessions = [self.legislative_session(session) for session in self.sessions()]

    def get_session_list(self):
        return [session['term_name'] for session in self.sessions()]

    def legislative_session(self, session):
        leg_session = {}
        start_year, end_year = session['term_name'].split('-')
        leg_session['identifier'] = session['term_name']
        leg_session['name'] = session['term_name']
        leg_session['start_date'] = '{}-12-01'.format(start_year)
        leg_session['end_date'] = '{}-11-30'.format(end_year)
        leg_session['classification'] = 'primary'

        return leg_session

    def sessions(self):
        response = requests.get('http://app.toronto.ca/tmmis/findAgendaItem.do?function=doPrepare')
        page = lxml.html.fromstring(response.text)
        # Remove the blank option label and sort chronologically
        for option in reversed(page.xpath('//select[@name="termId"][1]/option')[1:]):
            session = {}
            session['termId'] = option.attrib['value']
            session['term_name'] = option.text
            yield session
