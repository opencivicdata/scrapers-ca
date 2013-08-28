#!/usr/bin/python
# -*- coding: latin-1 -*-
from pupa.scrape import Scraper
from pupa.models import Event

from utils import lxmlize

import requests
import re
import datetime as dt
import csv
import tempfile
import shutil
import os


class TorontoEventScraper(Scraper):

  def get_events(self):
    "http://app.toronto.ca/tmmis/getAdminReport.do?function=prepareMeetingScheduleReport"
    "http://app.toronto.ca/tmmis/getAdminReport.do?function=prepareMemberAttendanceReport"

 # scrape attendance

    tmpdir = tempfile.mkdtemp()

    page = lxmlize("http://app.toronto.ca/tmmis/getAdminReport.do?function=prepareMemberAttendanceReport")
    members = page.xpath('//td[@class="inputText"]/select[@name="memberId"]/option')
    for member in members:
      post = {
        'function': 'getMemberAttendanceReport',
        'download': 'csv',
        'exportPublishReportId': 1,
        'termId': 4,
        'memberId': member.attrib['value'],
        'decisionBodyId': 0,
      }
      r = requests.post("http://app.toronto.ca/tmmis/getAdminReport.do", data=post)
      if r.headers['content-type'] != 'application/vnd.ms-excel':
        continue

      attendance_file = open(tmpdir + '/' + member.text + '.csv', 'w')
      attendance_file.write(r.text)
      attendance_file.close()

# scrape events
    post = {
      'function': 'getMeetingScheduleReport',
      'download': 'csv',
      'exportPublishReportId': 3,
      'termId': 4,
      'decisionBodyId': 0,
    }

    r = requests.post("http://app.toronto.ca/tmmis/getAdminReport.do", data=post)
    empty = []

    meeting_file = open('meetings.csv', 'w')
    meeting_file.write(r.text)
    meeting_file.close()
    with open('meetings.csv', 'rb') as csvfile:
      csvfile = csv.reader(csvfile, delimiter=',')
      next(csvfile)

      committee = ''
      agenda_items = []

      for row in csvfile:
        name = row[0]
        when = row[2]
        when = dt.datetime.strptime(when, "%Y-%m-%d")
        location = row[5]

        if name != committee:
          committee = name
          agenda_items = find_items(committee)

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

        for item in agenda_items:
          if item['date'].date() == when.date():
            i = e.add_agenda_item(item['description'])
            i.add_committee(committee)
            i['order'] = item['order']

            for link in item['links']:
              i.add_media_link(link['name'], link['url'], on_duplicate='ignore')

            if 'notes' in item:
              i['notes'] = [item['notes']]

        yield e

    shutil.rmtree(tmpdir)
    os.remove('meetings.csv')


def find_attendees(directory, event):
  # TODO
  # go through all csv files and find members that attended the event
  attendees = []
  files = [f for f in os.listdir(directory)]
  for f in files:
    name = f.replace('.csv', '')
    with open(directory + '/' + f, 'rb') as csvfile:
      csvfile = csv.reader(csvfile, delimiter=',')
      next(csvfile)
      for row in csvfile:
        # find the right date
        if row[2] == event[2]:
          if (row[0] == event[0]) and (row[1] == event[1]) and (row[5] == "Y"):
            attendees.append(name)
  return set(attendees)


def find_items(committee):

  agenda_items = []

  page = lxmlize('http://app.toronto.ca/tmmis/decisionBodyList.do?function=prepareDisplayDBList')
  link = page.xpath('//table[@class="default zebra"]//a[contains(text(),"%s")]/@href' % committee)
  if link:
    link = link[0]
  else:
    return None

  page = lxmlize(link)
  meetings = page.xpath('//a[contains(@name, "header")]')
  for meeting in meetings:
    if not 'Complete' in meeting.xpath('./parent::h3')[0].text_content():
      continue
    date = meeting.xpath('./parent::h3')[0].text_content().strip().split('-')
    date = dt.datetime.strptime('-'.join(date[0:2]).strip(), "%B %d, %Y - %I:%M %p")
    meeting_id = meeting.attrib['name'].replace('header', '').strip()
    # get = { 'function' : 'doPrepare', 'meetingId' : meeting_id }
    if committee == 'City Council':
      request_string = 'http://app.toronto.ca/tmmis/viewAgendaItemList.do?function=getCouncilAgendaItems&meetingId=%s' % meeting_id
    else:
      request_string = 'http://app.toronto.ca/tmmis/viewAgendaItemList.do?function=getAgendaItems&meetingId=%s' % meeting_id
    page = lxmlize(request_string)

    items = page.xpath('//tr[@class="nonUrgent" or @class="urgent"]')
    for item in items:
      page = lxmlize(item.xpath('.//a/@href')[0])
      item_content_script = page.xpath('//script[contains(text(), "loadContent")]/text()')[0]
      item_id = re.findall(r'(?<=agendaItemId:")(.*)(?=")', item_content_script)[0]
      if committee == 'City Council':
        item_info_url = 'http://app.toronto.ca/tmmis/viewAgendaItemDetails.do?function=getCouncilMinutesItemPreview&r=1376598367685&agendaItemId=%s' % item_id
      else:
        item_info_url = 'http://app.toronto.ca/tmmis/viewAgendaItemDetails.do?function=getMinutesItemPreview&r=1376593612354&agendaItemId=%s' % item_id
      page = lxmlize(item_info_url)

      root_description = page.xpath('//font[@size="4"]')[0].text_content()
      root_order = page.xpath('//table[@class="border"]//td[1]//text()')[0]

      # Get background documents
      item_links = []
      links = page.xpath('//a[not(contains(@href, "mailto:"))]')
      for link in links:
        if not 'href' in link.attrib.keys():
          continue
        description = link.xpath('.//parent::font/preceding-sibling::font/text()')
        if description:
          description = description[-1]
        else:
          description = link.text_content()
        item_link = {'name': description, 'url': link.attrib['href']}
        item_links.append(item_link)

      agenda_items.append({
        'committee': committee,
        'description': root_description,
        'order': root_order,
        'date': date,
        'links': item_links,
      })

      # Read through the decisions section and create agenda items from the list
      decisions = page.xpath('//b[contains(text(), "Decision")]/ancestor::tr/following-sibling::tr//p')
      agenda_item = {}
      notes = ''
      for decision in decisions:
        if 'style' in decision.attrib.keys() and 'MARGIN-LEFT: 1in' in decision.attrib['style']:
          note = decision.text_content().strip()
          notes = notes + ' ' + note
        if not decision.text_content().strip() or not re.findall(r'[0-9]\.\W{2,}', decision.text_content()):
          continue
        number = re.findall(r'([0-9]{1,2})\.', decision.text_content())[0]
        description = re.sub(r'^[0-9]{1,2}\.', '', decision.text_content()).strip()
        order = root_order + '-' + number

        agenda_item['committee'] = committee
        agenda_item['description'] = description
        if len(notes) > 0:
          agenda_item['notes'] = {'description': notes}
        agenda_item['order'] = order
        agenda_item['date'] = date
        agenda_item['links'] = item_links
        agenda_items.append(agenda_item)
        agenda_item = {}
        notes = ''

  return agenda_items
