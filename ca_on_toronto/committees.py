from __future__ import unicode_literals
from utils import CanadianScraper
from pupa.scrape import Organization
from .helpers import build_lookup_dict, committees_from_sessions
from .constants import TWO_LETTER_ORG_CODE_SCHEME

import re


MEMBERS_URL_TEMPLATE = 'http://app.toronto.ca/tmmis/decisionBodyProfile.do?function=doGetMembers&meetingId={}&showLink=true'
DEFAULT_COMMITTEE_ROLE = 'Member'

REFERENCE_MEETING_IDS = {
        'AU': 11008,
        'HL': 10899,
        'CA': 10868,
        'CD': 10948,
        'ED': 10972,
        'EX': 10989,
        'GM': 10881,
        'LS': 10979,
        'PE': 10940,
        'PG': 10957,
        'PW': 10964,
        'ST': 11568,
        }

class TorontoCommitteeScraper(CanadianScraper):
    def allMembers(self, member_list_url):
        members = []

        page = self.lxmlize(member_list_url)
        for li in page.xpath('//ul/li'):
            member = {'is_councillor': False}

            if li.xpath('.//a'): member['is_councillor'] = True

            li_re = re.compile(r'^(?P<name>.+?)(?: \((?P<role>.+)\))?$')
            li_text = li.text_content().strip()
            matches = re.match(li_re, li_text)

            role = matches.group('role')
            member['role'] = role if role else DEFAULT_COMMITTEE_ROLE
            member['name'] = matches.group('name').strip()

            yield member

    def councillorMembers(self, org_code):
        ref_meeting_id = REFERENCE_MEETING_IDS.get(org_code)
        if ref_meeting_id:
            membership_url = MEMBERS_URL_TEMPLATE.format(ref_meeting_id)
            for member in self.allMembers(membership_url):
                if member['is_councillor']: yield member
                # TODO: Scrape non-councillor members


    def scrape(self):
        sessions = reversed(self.jurisdiction.legislative_sessions)
        committee_term_instances = committees_from_sessions(self, sessions)
        committees_by_code = build_lookup_dict(self, data_list=committee_term_instances, index_key='code')

        for code, instances in committees_by_code.items():
            # TODO: Figure out how to edit city council org.
            if code == 'CC':
                continue

            extras = {'tmmis_decision_body_ids': []}
            for i, inst in enumerate(instances):
                # TODO: Ensure this survives addition of new term (2017)
                #       so specific year always creates
                canonical_i = 0
                if i == canonical_i:
                    o = Organization(name=inst['name'], classification='committee')
                    extras.update({'description': inst['info']})
                    o.add_identifier(inst['code'], scheme=TWO_LETTER_ORG_CODE_SCHEME)

                    print(inst['code'])

                    for councillor in self.councillorMembers(inst['code']):
                        o.add_member(councillor['name'], councillor['role'])

                extras['tmmis_decision_body_ids'].append({inst['term']: inst['decision_body_id']})
                o.extras = extras
                o.add_source(inst['source_url'])
                if instances[canonical_i]['name'] != inst['name']:
                    # TODO: Add start_date and end_date
                    o.add_name(inst['name'])

            yield o
