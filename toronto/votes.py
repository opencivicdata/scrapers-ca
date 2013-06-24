from pupa.scrape import Scraper
from larvae.vote import Vote

from .utils import lxmlize
import requests, re


class TorontoVoteScraper(Scraper):
  def get_votes(self):
    "http://app.toronto.ca/tmmis/getAdminReport.do?function=prepareMemberVoteReport"
    page = lxmlize("http://app.toronto.ca/tmmis/getAdminReport.do?function=prepareMemberVoteReport")

    members = page.xpath('//td[@class="inputText"]/select[@name="memberId"]/option')
    for member in members:
      if not member in members[0:2]:
        continue
      post = {
      'function' : 'getMemberVoteReport',
      'download': 'csv',
      'exportPublishReportId' : 2,
      'termId' : 4,
      'memberId' : member.attrib['value'],
      'decisionBodyId' : 0,
      
      }

      r = requests.post("http://app.toronto.ca/tmmis/getAdminReport.do", data=post)
      if r.headers['content-type'] == 'application/vnd.ms-excel':
        for row in re.split("[^r]\\n",r.text)[1:]: 

          row = row.split('\",\"')
          if not row or len(row) < 8:
            continue

          session = self.session
          date = row[1].split()[0]
          v_type = map_type(row[4])
          passed = 'Carried' in row[6]

          if not 'tie' in row[6]:  
            yes_count, no_count = row[6].split()[1].split('-')  
          else:
            yes_count, no_count = 1, 1
          vote = Vote(session, date, v_type, passed, int(yes_count), int(no_count))
          vote.vote(member.text.strip(), row[5].lower())
#          vote.add_bill(row[3],chamber=None)
          vote.add_source("http://app.toronto.ca/tmmis/getAdminReport.do")
          yield vote

def map_type(type_string):
  if "Amend" in type_string:
    return "amendment"
  if "Adopt" in type_string:
    return "passage"