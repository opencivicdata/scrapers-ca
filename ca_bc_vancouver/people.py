# coding: utf-8
from pupa.scrape import Scraper

from utils import csv_reader, CanadianLegislator as Legislator

import re

COUNCIL_PAGE = 'ftp://webftp.vancouver.ca/OpenData/csv/CouncilContactInformation.csv'

class VancouverPersonScraper(Scraper):

  def get_people(self):
    for row in csv_reader(COUNCIL_PAGE, header=True):
      p = Legislator(
        name='%(First Name)s %(Last Name)s' % row,
        post_id='Vancouver',
        role=row['Elected Office'],
        gender=row['Gender'],
        image=row['Photo URL'],
      )
      p.add_contact('email', row['Email'], None)
      p.add_contact('voice', row['Phone'], 'legislature')
      p.add_contact('fax', row['Fax'], 'legislature')
      p.add_contact('address', '%(Address line 1)s\n%(Locality)s %(Province)s %  %(Postal Code)s' % row, 'legislature')
      p.add_source(COUNCIL_PAGE)
      p.add_source(row['URL'])
      yield p
