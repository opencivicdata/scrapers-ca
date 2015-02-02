from __future__ import unicode_literals
from utils import CanadianJurisdiction

import lxml.html
import requests


class Toronto(CanadianJurisdiction):
    classification = 'legislature'
    division_id = 'ocd-division/country:ca/csd:3520005'
    division_name = 'Toronto'
    name = 'Toronto City Council'
    url = 'http://www.toronto.ca'

    def get_session_list(self):
        response = requests.get('http://app.toronto.ca/tmmis/getAdminReport.do?function=prepareMemberVoteReport')
        return lxml.html.fromstring(response.text).xpath('//select[@name="termId"][1]/option/text()')
