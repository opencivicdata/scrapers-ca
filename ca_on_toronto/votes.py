# -*- coding: utf-8 -*-
from pupa.scrape import Scraper
from pupa.models import Vote

from utils import lxmlize
import requests
import re
import csv
import tempfile
import shutil
import os

VOTES = {'Yes': 'yes', 'No': 'no', 'Absent': 'not-voting'}


class TorontoVoteScraper(Scraper):

  def get_votes(self):

    tmpdir = tempfile.mkdtemp()
    download_files(tmpdir)

    # read through each csv file
    files = [f for f in os.listdir(tmpdir)]
    for f in files:

      name = f.replace('.csv', '')

      with open(tmpdir + '/' + f, 'rb') as csvfile:
        csvfile = csv.reader(csvfile, delimiter=',')
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
          scan_files(tmpdir, f, vote, row)
          vote.add_source("http://app.toronto.ca/tmmis/getAdminReport.do")
          yield vote
      os.remove(tmpdir + '/' + f)
    shutil.rmtree(tmpdir)


def download_files(dest_directory):
  "http://app.toronto.ca/tmmis/getAdminReport.do?function=prepareMemberVoteReport"
  page = lxmlize("http://app.toronto.ca/tmmis/getAdminReport.do?function=prepareMemberVoteReport")

  # download csv files
  members = page.xpath('//td[@class="inputText"]/select[@name="memberId"]/option')
  for member in members:

    post = {
        'function': 'getMemberVoteReport',
        'download': 'csv',
        'exportPublishReportId': 2,
        'termId': 4,
        'memberId': member.attrib['value'],
        'decisionBodyId': 0,

    }

    r = requests.post("http://app.toronto.ca/tmmis/getAdminReport.do", data=post)
    if r.headers['content-type'] != 'application/vnd.ms-excel':
      continue

    name = member.text
    if name == "Norman Kelly":
      name = "Norm Kelly"
    if "Ana Bail" in name:
      name = "Ana Bailao"

    print 'downloading ' + name

    vote_file = open(dest_directory + '/' + name + '.csv', 'w')
    vote_file.write(r.text.encode('utf-8').strip())
    vote_file.close()


# scan csv files of other representatives for matching votes
# adding representatives to Vote object
# delete matching rows in other files
def scan_files(directory, current_file, vote, vote_row):
  files = [f for f in os.listdir(directory)]
  for f in files:
    if f == current_file:
      continue
    name = f.replace('.csv', '')
    tempfile_target = open(directory + '/temp.csv', 'wb')
    tempfile = csv.writer(tempfile_target)
    with open(directory + '/' + f, 'r+') as csvfile:
      csvfile = csv.reader(csvfile, delimiter=',')
      for row in csvfile:
        row_description = row[2:5] + row[6:8]
        vote_description = vote_row[2:5] + vote_row[6:8]
        if (row_description == vote_description):
          vote.vote(name, VOTES[row[5]])
        else:
          tempfile.writerow(row)
      tempfile_target.close()

    os.remove(directory + '/' + f)
    os.rename(directory + '/temp.csv', directory + '/' + f)
