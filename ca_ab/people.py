# coding: utf-8
from __future__ import unicode_literals
from pupa.scrape import Scraper

import re
import csv

import lxml.html
from lxml import etree

from utils import CanadianScraper, CanadianPerson as Person

COUNCIL_PAGE = 'http://www.assembly.ab.ca/net/index.aspx?p=mla_csv'

PARTIES = {
    'AL': 'Alberta Liberal Party',
    'ND': 'Alberta New Democratic Party',
    'PC': 'Progressive Conservative Association of Alberta',
    'W': 'Wildrose Alliance Party',
    'IND': 'Independent',
}


def get_party(abbr):
  """Return full party name from abbreviation"""
  return PARTIES[abbr]


class AlbertaPersonScraper(CanadianScraper):

  def scrape(self):
    csv_text = self.get(self.get_csv_url()).text
    cr = csv.DictReader(csv_text.split('\n'))
    for mla in cr:
      name = '%s %s %s' % (mla['MLA First Name'], mla['MLA Middle Names'],
                           mla['MLA Last Name'])
      if name.strip() == '':
          continue
      party = get_party(mla['Caucus'])
      name_without_status = name.split(',')[0]
      p = Person(primary_org='legislature', name=name_without_status, district=mla['Riding Name'],
                     role='MLA', party=party)
      p.add_source(COUNCIL_PAGE)
      p.add_contact('email', mla['Email'])
      if mla['Phone Number']:
          p.add_contact('voice', mla['Phone Number'], 'legislature')
      yield p

  def get_csv_url(self):
    csv_gen_page = self.lxmlize(COUNCIL_PAGE)

    # ASP forms store session state. Looks like we can't just play back a POST.
    get_hidden_val = lambda p, v: p.xpath('string(//input[@id="%s"]/@value)' % v)
    asp_viewstate = get_hidden_val(csv_gen_page, '__VIEWSTATE')
    asp_event_validation = get_hidden_val(csv_gen_page, '__EVENTVALIDATION')
    post_data = {
      '_ctl0:radlstGroup': 'Information for All MLAs',
      '_ctl0:chklstFields:0': 'on',
      '_ctl0:chklstFields:1': 'on',
      '_ctl0:chklstFields:2': 'on',
      '_ctl0:btnCreateCSV': "Create '.csv' file",
      '__VIEWSTATE': asp_viewstate,
      '__EVENTVALIDATION': asp_event_validation
    }

    resp = self.post(COUNCIL_PAGE, data=post_data)
    result_page = lxml.html.fromstring(resp.text)
    return result_page.xpath('string(//a[@id="_ctl0_HL_file"]/@href)')
