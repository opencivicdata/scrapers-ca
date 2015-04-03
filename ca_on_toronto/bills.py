from __future__ import unicode_literals

import csv
import re
from collections import defaultdict
from datetime import datetime

from pupa.scrape import Bill, Vote
from six import StringIO
from utils import CanadianScraper

SOURCE_URL = 'http://app.toronto.ca/tmmis/getAdminReport.do?function=prepareMemberVoteReport'

result_re = re.compile('^(Carried|Lost(?: \(tie\))?), (\d+)-(\d+)$')
quorum_re = re.compile('^(Majority Required|Two-Thirds Required|Two-Thirds full Council Required) - (.+)')

result_map = {
    'Carried': 'pass',
    'Lost': 'fail',
    'Lost (tie)': 'fail',
}
vote_map = {
    'Yes': 'yes',
    'No': 'no',
    'Absent': 'absent',
}


class TorontoBillScraper(CanadianScraper):
    def scrape(self):
        # We store agenda items as bills, because Pupa can only have votes on
        # bills. Toronto has no bills anyhow.

        # Toronto groups voting records by member, but Pupa expects them to be
        # grouped by vote event. In order to group voting records by vote event,
        # we need to know how to uniquely identify a vote event.
        #
        # To do so, we write a CSV of all voting records. special_snowflake can
        # find unique keys in CSVs, but it doesn't fail fast and is thus slow.
        # We use Ruby's fastcsv and lycopodium gems instead.
        #
        # require 'fastcsv'
        # require 'lycopodium'
        # Lycopodium.unique_key(FastCSV.read('out.csv'))
        #
        # The unique key is: Voter, Date/Time, Agenda Item #, Vote Description.

        # The open data catalog has a data dictionary for the CSV columns.
        # @see http://www1.toronto.ca/wps/portal/contentonly?vgnextoid=b93709401385d210VgnVCM1000003dd60f89RCRD&vgnextchannel=1a66e03bb8d1e310VgnVCM10000071d60f89RCRD
        page = self.lxmlize(SOURCE_URL)
        for term in page.xpath('//select[@name="termId"][1]/option'):
            bills = {}
            vote_events = {}
            votes = defaultdict(list)
            for member in page.xpath('//select[@name="memberId"]/option[position()>1]'):
                response = self.post('http://app.toronto.ca/tmmis/getAdminReport.do', data={
                    'function': 'getMemberVoteReport',
                    'download': 'csv',
                    'termId': term.attrib['value'],
                    'memberId': member.attrib['value'],
                })

                response.encoding = 'windows-1252'

                for row in csv.DictReader(StringIO(response.text)):
                    # @todo Sent request to City clerk about unique keys for other organizations.
                    if row['Committee'] == 'City Council':
                        if len(row['Date/Time']) == 10:
                            start_date = str(datetime.strptime(row['Date/Time'], '%Y-%m-%d'))
                        else:
                            start_date = str(datetime.strptime(row['Date/Time'], '%Y-%m-%d %H:%M %p'))

                        result_match = result_re.search(row['Result'])

                        # The "Vote Description":
                        # * includes a version of the "Motion Type", which may add
                        #   the member being nominated, for example
                        # * may repeat the "Agenda Item #"
                        # * may include the parts of the agenda item being voted on
                        # * may include the motion's identifier
                        # * may include the motion's creator
                        # @note Unused, because OpenCivicData has no field for quorum, etc.
                        quorum_match = quorum_re.search(row['Vote Description'])

                        bill_key = row['Agenda Item #']
                        bill = {
                            'legislative_session': term.text,
                            'identifier': row['Agenda Item #'],
                            'title': row['Agenda Item Title'],
                        }
                        if bills.get(bill_key):
                            if bills[bill_key] != bill:
                                raise Exception('bill mismatch {} != {}'.format(repr(bills[bill_key]), repr(bill)))
                        else:
                            bills[bill_key] = bill

                        vote_event_key = tuple([row['Date/Time'], row['Agenda Item #'], row['Vote Description']])
                        vote_event = {
                            'bill': row['Agenda Item #'],
                            'legislative_session': term.text,
                            'start_date': start_date,
                            'motion_text': row['Vote Description'],  # @todo not motion text
                            'classification': row['Motion Type'],
                            'result': result_map[result_match.group(1)],
                            'counts': (int(result_match.group(2)), int(result_match.group(3)))
                        }
                        if vote_events.get(vote_event_key):
                            if vote_events[vote_event_key] != vote_event:
                                raise Exception('vote event mismatch {} != {}'.format(repr(vote_events[vote_event_key]), repr(vote_event)))
                        else:
                            vote_events[vote_event_key] = vote_event

                        votes[vote_event_key].append({
                            'option': vote_map[row['Vote']],
                            'voter_name': member.text,
                        })

                # To write a CSV instead. Delete and touch out.csv before starting.
                #
                # with open('out.csv', 'a') as f:
                #     writer = csv.writer(f)
                #     reader = csv.reader(StringIO(response.text))
                #     next(reader)
                #     for row in reader:
                #         # Other organizations may contain duplicate rows, for
                #         # example: 2010-2014, Paul Ainslie, 2011.ZB9.1.
                #         if row[0] == 'City Council':
                #             row.insert(0, term.text)
                #             row.insert(1, member.text)
                #             writer.writerow(row)

            for key, properties in bills.items():
                b = Bill(**properties)
                b.add_source(SOURCE_URL)

                yield b

            for key, properties in vote_events.items():
                counts = properties.pop('counts')
                v = Vote(**properties)
                v.set_count('yes', counts[0])
                v.set_count('no', counts[1])
                v.add_source(SOURCE_URL)
                for vote in votes[key]:
                    v.vote(vote['option'], vote['voter_name'])

                yield v
