# coding: utf-8
from pupa.scrape import Scraper

from utils import lxmlize, CanadianLegislator as Legislator

import re

from urllib2 import urlopen
from csv import DictReader

COUNCIL_CSV_URL = 'http://data.ottawa.ca/en/storage/f/2013-10-29T130227/Elected-Officials-%282010-2014%29-v.3.csv'


class OttawaPersonScraper(Scraper):

  def get_people(self):
      response = urlopen(COUNCIL_CSV_URL)
      cr = DictReader(response)
      for councillor in cr:
        name = '%s %s' % (councillor['First name'], councillor['Last name'])
        district = councillor['District name'] or None
        role = councillor['Elected office']
        email = councillor['Email']
        address = ', '.join([councillor['Address line 1'],
                             councillor['Address line 2'],
                             councillor['Locality'],
                             councillor['Postal code'],
                             councillor['Province']])
        phone = councillor['Phone']
        photo_url = councillor['Photo URL']

        p = Legislator(name=name, post_id=district, role=role)
        p.add_source(COUNCIL_CSV_URL)
        p.add_contact('email', email, None)
        p.add_contact('address', address, 'Legislature')
        p.add_contact('voice', phone, 'Legislature')
        p.image = photo_url
        yield p

