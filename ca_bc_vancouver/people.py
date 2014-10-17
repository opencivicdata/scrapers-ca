# coding: utf-8
from __future__ import unicode_literals
from pupa.scrape import Scraper

import re

from utils import CanadianScraper, CanadianPerson as Person

COUNCIL_PAGE = 'ftp://webftp.vancouver.ca/OpenData/csv/CouncilContactInformation.csv'


class VancouverPersonScraper(CanadianScraper):

    def scrape(self):
        for row in self.csv_reader(COUNCIL_PAGE, header=True):
            p = Person(
                primary_org='legislature',
                name='%(First Name)s %(Last Name)s' % row,
                district='Vancouver',
                role=row['Elected Office'],
                gender=row['Gender'],
                image=row['Photo URL'],
            )
            p.add_contact('email', row['Email'])
            p.add_contact('voice', row['Phone'], 'legislature')
            p.add_contact('fax', row['Fax'], 'legislature')
            p.add_contact('address', '%(Address line 1)s\n%(Locality)s %(Province)s  %(Postal Code)s' % row, 'legislature')
            p.add_source(COUNCIL_PAGE)
            p.add_source(row['URL'])
            yield p
