from pupa.scrape import Scraper
from larvae.vote import Vote

from .utils import lxmlize
import requests, re
import csv, tempfile, shutil, os

VOTES = {'Yes':'yes', 'No':'no', 'Absent':'not-voting'}

class TorontoVoteScraper(Scraper):



  def get_votes(self):
    vote_no = 0
    "http://app.toronto.ca/tmmis/getAdminReport.do?function=prepareMemberVoteReport"
    page = lxmlize("http://app.toronto.ca/tmmis/getAdminReport.do?function=prepareMemberVoteReport")

    tmpdir = tempfile.mkdtemp()


    members = page.xpath('//td[@class="inputText"]/select[@name="memberId"]/option')
    for member in members:
      if member not in members[1:3]:
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
      if r.headers['content-type'] != 'application/vnd.ms-excel':
        continue

      print 'downloading '+member.text

      vote_file = open(tmpdir+'/'+member.text+'.csv','w')
      vote_file.write(r.text.encode('utf-8').strip())
      vote_file.close()


    files = [f for f in os.listdir(tmpdir)]
    for f in files:
      name = f.replace('.csv','')
      with open(tmpdir+'/'+f,'rb') as csvfile:
        csvfile = csv.reader(csvfile, delimiter = ',')
        next(csvfile)
        for row in csvfile:
          session = self.session
          date = row[1].split()[0]
          v_type = 'other'
          passed = 'Carried' in row[6] 
          if not 'tie' in row[6]:  
            yes_count, no_count = row[6].split()[1].split('-')  
          else:
            yes_count, no_count = 1, 1
          vote = Vote(session, date, row[3], v_type, passed, int(yes_count), int(no_count))
          vote.vote(name, VOTES[row[5]])
          find_voters(tmpdir, f, vote, row)
          vote.add_source("http://app.toronto.ca/tmmis/getAdminReport.do")
          vote_no = vote_no+1
          yield vote
      os.remove(tmpdir+'/'+f)
    shutil.rmtree(tmpdir)

def find_voters(directory, current_file, vote, vote_row):
  members = []
  files = [f for f in os.listdir(directory)]
  for f in files:
    if f == current_file:
      continue
    name = f.replace('.csv','')

    tempfile = csv.writer(open(directory+'/temp.csv','wb'))
    with open(directory+'/'+f, 'r+') as csvfile:
      csvfile = csv.reader(csvfile, delimiter = ',')
      next(csvfile)
      for row in csvfile:
        if row[0] != vote_row[0]:
          tempfile.writerow(row)
          continue
        if same_vote(row, vote_row):
          vote.vote(name,VOTES[row[5]])
        else:
          tempfile.writerow(row)
    os.remove(directory+'/'+f)
    os.rename(directory+'/temp.csv',directory+'/'+f)


def same_vote(row1, row2):
  for i in range(1,7):
    if i == 5:
      continue
    if row1[i] != row2[i]:
      return False
  return True    



#     for row in re.split("[^r]\\n",r.text)[1:]: 

#       row = row.split('\",\"')
#       if not row or len(row) < 8:
#         continue

#       name = member.text.strip()
#       if name == "Norman Kelly":
#         name = "Norm Kelly"  
#       session = self.session
#       date = row[1].split()[0]
#       v_type = 'other' #map_type(row[4])
#       passed = 'Carried' in row[6]

#       if not 'tie' in row[6]:  
#         yes_count, no_count = row[6].split()[1].split('-')  
#       else:
#         yes_count, no_count = 1, 1
#       vote = Vote(session, date, row[3], v_type, passed, int(yes_count), int(no_count))
#       vote.vote(name, votes[row[5]])
# #          vote.add_bill(row[3],chamber=None)
#       vote.add_source("http://app.toronto.ca/tmmis/getAdminReport.do")
#       yield vote

