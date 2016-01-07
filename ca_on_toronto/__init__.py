from __future__ import unicode_literals
from .jurisdiction import TorontoJurisdiction
from .constants import CANONICAL_COUNCIL_NAME

import lxml.html
import requests


class Toronto(TorontoJurisdiction):
    classification = 'legislature'
    division_id = 'ocd-division/country:ca/csd:3520005'
    division_name = 'Toronto'
    name = CANONICAL_COUNCIL_NAME
    url = 'http://www.toronto.ca'
    use_type_id = True
    check_sessions = True
    legislative_sessions = [
        # TODO: Accommodate legacy format pages. (bad old PDF days)
        # {'identifier': '1998-2000'},
        # {'identifier': '2000-2003'},
        # {'identifier': '2003-2006'},
        {
            'identifier': '2006-2010',
            'name': '2006-2010',
            'start_date': '2006-12-01',
            'end_date': '2010-11-30',
            'classification': 'primary',
        },
        {
            'identifier': '2010-2014',
            'name': '2010-2014',
            'start_date': '2010-12-01',
            'end_date': '2014-11-30',
            'classification': 'primary',
        },
        {
            'identifier': '2014-2018',
            'name': '2014-2018',
            'start_date': '2014-12-01',
            'end_date': '2018-11-30',
            'classification': 'primary',
        },
    ]

    def get_session_list(self):
        response = requests.get('http://app.toronto.ca/tmmis/getAdminReport.do?function=prepareMemberVoteReport')
        return lxml.html.fromstring(response.text).xpath('//select[@name="termId"][1]/option/text()')
