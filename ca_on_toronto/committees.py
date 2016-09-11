from __future__ import unicode_literals
from collections import defaultdict
from pupa.scrape import Organization
from utils import CanadianScraper

from .helpers import build_lookup_dict, committees_from_sessions
from .constants import TWO_LETTER_ORG_CODE_SCHEME

import re


MEMBERSHIP_URL_TEMPLATE = 'http://app.toronto.ca/tmmis/decisionBodyProfile.do?function=doGetMembers&meetingId={}&showLink=true'
DEFAULT_COMMITTEE_ROLE = 'Member'


"""
The IDs were chosen by sampling the meeting AJAX links on each committee page,
while monitoring the right-hand column for changes in membership. We find a
meeting with maximum information about roles. On finding one, we inspect the
HTML element of that meeting's header for a class called `header<MEETING_ID>`,
which we use in this lookup dict.

"""
# TODO: Improve on this later for more dynamicism.
REFERENCE_MEETING_IDS = defaultdict(dict)
REFERENCE_MEETING_IDS['2014-2018'] = {
    # Standing Committees
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
    # Community Councils
    'EY': 10933,
    'NY': 10924,
    'SC': 10917,
    'TE': 10909,
    # Other Boards and Committees
    # 'AA': 0,  # TODO: no membership?
    'AH': 10469,
    # 'BD': 0,  # TODO: no membership?
    'CT': 11408,
    'HB': 11229,
    'SL': 11212,
    'TA': 11308,
    'AC': 11448,
    'HP': 11388,
    'HU': 11003,
    # '??': 0,  # TODO: Board of Health Public Health Champion Awards Selection Committee
    'HF': 11268,
    'ZB': 11250,
    'BU': 11060,
    'BW': 11138,
    'BV': 11135,
    'TS': 11154,
    'EA': 11430,
    'DB': 11608,
    'DI': 11288,
    'EL': 10668,
    'XK': 10249,
    'FA': 11097,
    'XJ': 10328,
    # 'GP': 0,  # TODO: no membership?
    'XQ': 9996,
    'XS': 10049,
    'XT': 10471,
    'XP': 9995,
    'XN': 9920,
    'XR': 10048,
    'XU': 10271,
    'LL': 10669,
    'XL': 11369,
    'AF': 10288,
    'XM': 10254,
    'NT': 11470,
    'NA': 10189,
    'NC': 11349,
    'NE': 11332,
    'NF': 10888,
    'NQ': 10768,
    'PY': 9922,
    'SV': 9937,  # TODO: chair not currently marked?
    'SY': 11169,
    'SX': 11194,
    'SZ': 11035,
    'PS': 10808,
    'SD': 11272,
    'TD': 11389,
    'FB': 11333,
    'MA': 11211,
    'PB': 11031,
}


class TorontoCommitteeScraper(CanadianScraper):

    def allMembers(self, member_list_url):
        """
        Return a list of dicts representing all members of an organization,
        including councillors, city staff, and public appointments.

        obj keys:
        * name (string)
        * role (string)
        * is_councillor (bool)
        """

        page = self.lxmlize(member_list_url)
        li_re = re.compile(r'^(?P<name>.+?)(?: \((?P<role>.+)\))?$')
        for li in page.xpath('//ul/li'):
            li_text = li.text_content().strip()
            matches = re.match(li_re, li_text)
            role = matches.group('role')

            member = {
                'role': role if role else DEFAULT_COMMITTEE_ROLE,
                'name': matches.group('name').strip(),
                'is_councillor': bool(li.xpath('.//a')),
            }

            yield member

    def councillorMembers(self, membership_url):
        """
        Return a list of dicts representing all councillor members of an
        organization.

        obj keys:
        * name (string)
        * role (string)
        * is_councillor (bool)
        """
        for member in self.allMembers(membership_url):
            if member['is_councillor']:
                yield member

    def referenceMeetingId(self, org_code, term='2014-2018'):
        """
        Returns a referencial meetingId for a given committee in a given term.
        """
        return REFERENCE_MEETING_IDS[term].get(org_code)

    def scrape(self):
        sessions = reversed(self.jurisdiction.legislative_sessions)
        committee_term_instances = committees_from_sessions(self, sessions)
        committees_by_code = build_lookup_dict(self, data_list=committee_term_instances, index_key='code')

        for code, instances in committees_by_code.items():
            # TODO: Figure out how to edit city council org.
            if code == 'CC':
                continue

            # When there are no meetings scheduled and was no way to deduce committee code.
            if not code:
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

                    # TODO: Scrape non-councillor members
                    meeting_id = self.referenceMeetingId(inst['code'], inst['term'])
                    if meeting_id:
                        seen_posts = []
                        membership_url = MEMBERSHIP_URL_TEMPLATE.format(meeting_id)
                        for councillor in self.councillorMembers(membership_url):
                            o.add_member(councillor['name'], councillor['role'])
                            if councillor['role'] not in seen_posts:
                                # TODO: More specific divisions for some committee?
                                o.add_post(role=councillor['role'], label=councillor['role'], division_id=self.jurisdiction.division_id)
                                seen_posts.append(councillor['role'])

                extras['tmmis_decision_body_ids'].append({inst['term']: inst['decision_body_id']})
                o.extras = extras
                o.add_source(inst['source_url'])
                if instances[canonical_i]['name'] != inst['name']:
                    # TODO: Add start_date and end_date
                    o.add_name(inst['name'])

            yield o
