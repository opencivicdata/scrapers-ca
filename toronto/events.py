from pupa.scrape import Scraper
from larvae.event import Event

from .utils import lxmlize

import requests, re
import datetime as dt

class TorontoEventScraper(Scraper):
  def get_events(self):
    "http://app.toronto.ca/tmmis/getAdminReport.do?function=prepareMeetingScheduleReport"
    "http://app.toronto.ca/tmmis/getAdminReport.do?function=prepareMemberAttendanceReport"

 ############## scrape attendance
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
   if r.headers['content-type'] == 'application/vnd.ms-excel':
     for row in re.split("[^r]\\n",r.text)[1:]: 
       if not row:
         continue
       print row
       row = row.split('\",\"')

       ### write each row to a csv, save csv with the members name

############### scrape events

    post = {
      'function' : 'getMeetingScheduleReport',
      'download' : 'csv',
      'exportPublishReportId' : 3,
      'termId' : 4,
      'decisionBodyId': 0,
    }

    things = []
    r = requests.post("http://app.toronto.ca/tmmis/getAdminReport.do", data=post)
  #  if r.headers['content-type'] == 'application/vnd.ms-excel':
    
    for row in re.split("[^r]\\n",r.text)[1:]:
      if not row:
        continue
      row = row.split('\",\"')
      name = row[0]
      when = row[2]
      when = dt.datetime.strptime(when, "%Y-%m-%d")

      location = row[5] 
      print when     
      e = Event(name=name,
                session=self.session,
                when=when,
                location=location
        )
      e.add_source("http://app.toronto.ca/tmmis/getAdminReport.do?function=prepareMeetingScheduleReport")
      yield e

  def  find_attendees(event):
    #TODO
    #go through all csv files and find members that attended the event 
