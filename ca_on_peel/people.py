# coding: utf-8
from pupa.scrape import Scraper

from utils import csv_reader, CanadianLegislator as Legislator

import re

COUNCIL_PAGE = 'http://opendata.peelregion.ca/media/25713/ward20102014_csv_12.2013.csv'

class PeelPersonScraper(Scraper):

  def get_people(self):
    for row in csv_reader(COUNCIL_PAGE, header=True, headers={'Cookie': 'incap_ses_168_68279=7jCHCh608QQSFVti3dtUAviu/1IAAAAAIRf6OsZL0NttnlzANkVb6w=='}):
      p = Legislator(
        name='%(FirstName0)s %(LastName0)s' % row,
        post_id='%(MUNIC)s Ward %(WARDNUM)s' % row,
        role='Councillor',
      )
      p.add_contact('email', row['email0'], None)
      p.add_contact('voice', row['Phone0'], 'legislature')
      p.add_source(COUNCIL_PAGE)
      yield p

      if row['FirstName1'].strip():
        p = Legislator(
          name='%s %s' % (row['FirstName1'], row['LastName1']),
          post_id='%(MUNIC)s Ward %(WARDNUM)s' % row,
          role='Councillor',
        )
        p.add_contact('email', row['email1'], None)
        p.add_contact('voice', row['Phone1'], 'legislature')
        p.add_source(COUNCIL_PAGE)
        yield p
