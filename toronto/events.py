from pupa.scrape import Scraper
from larvae.event import Event

from .utils import lxmlize

import requests, re
import datetime as dt
import csv, tempfile, shutil
import os

class TorontoEventScraper(Scraper):
  def get_events(self):
    "http://app.toronto.ca/tmmis/getAdminReport.do?function=prepareMeetingScheduleReport"
    "http://app.toronto.ca/tmmis/getAdminReport.do?function=prepareMemberAttendanceReport"

 ############## scrape attendance

    tmpdir = tempfile.mkdtemp()

    page = lxmlize("http://app.toronto.ca/tmmis/getAdminReport.do?function=prepareMemberAttendanceReport")
    members = page.xpath('//td[@class="inputText"]/select[@name="memberId"]/option')
    for member in members:
      post = {
        'function' : 'getMemberAttendanceReport',
        'download' : 'csv',
        'exportPublishReportId' : 1,
        'termId' : 4,
        'memberId' : member.attrib['value'],
        'decisionBodyId' : 0,
      }
      r = requests.post("http://app.toronto.ca/tmmis/getAdminReport.do", data=post)
      if r.headers['content-type'] != 'application/vnd.ms-excel':
        continue

      attendance_file = open(tmpdir+'/'+member.text+'.csv', 'w')
      attendance_file.write(r.text)
      attendance_file.close()


############### scrape events

    post = {
      'function' : 'getMeetingScheduleReport',
      'download' : 'csv',
      'exportPublishReportId' : 3,
      'termId' : 4,
      'decisionBodyId': 0,
    }

    r = requests.post("http://app.toronto.ca/tmmis/getAdminReport.do", data=post)
    empty = []

    meeting_file = open('meetings.csv','w')
    meeting_file.write(r.text)
    meeting_file.close()
    with open('meetings.csv','rb') as csvfile:
      csvfile = csv.reader(csvfile,delimiter = ',')
      next(csvfile)
      for row in csvfile:
        name = row[0]
        when = row[2]
        when = dt.datetime.strptime(when, "%Y-%m-%d")
        location = row[5] 

        e = Event(name=name,
                  session=self.session,
                  when=when,
                  location=location
          )
        
        attendees = find_attendees(tmpdir, row)
        if len(attendees) == 0:
          empty.append(row)
        for attendee in find_attendees(tmpdir, row):
          e.add_person(attendee)
        e.add_source("http://app.toronto.ca/tmmis/getAdminReport.do?function=prepareMeetingScheduleReport")
        yield e

    shutil.rmtree(tmpdir)
    os.remove('meetings.csv')

def find_attendees(directory , event):
  # TODO
  # go through all csv files and find members that attended the event
  attendees = [] 
  files = [f for f in os.listdir(directory)]
  for f in files:
    name = f.replace('.csv','')
    with open(directory+'/'+f,'rb') as csvfile:
      csvfile = csv.reader(csvfile, delimiter = ',')
      next(csvfile)
      for row in csvfile:
        ## find the right date
        if row[2] == event[2]:
          if (row[0] == event[0]) and (row[1] == event[1]) and (row[5] == "Y"):
            attendees.append(name)
  return set(attendees)


