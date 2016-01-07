from __future__ import unicode_literals
from utils import CanadianScraper
from pupa.scrape import Organization
from .helpers import build_lookup_dict, committees_from_sessions
from .constants import TWO_LETTER_ORG_CODE_SCHEME


class TorontoCommitteeScraper(CanadianScraper):
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
                extras['tmmis_decision_body_ids'].append({inst['term']: inst['decision_body_id']})
                o.extras = extras
                o.add_source(inst['source_url'])
                if instances[canonical_i]['name'] != inst['name']:
                    # TODO: Add start_date and end_date
                    o.add_name(inst['name'])

            yield o
