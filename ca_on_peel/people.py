# coding: utf-8
from pupa.scrape import Scraper

from utils import lxmlize, csv_reader, CanadianLegislator as Legislator

import re

COUNCIL_PAGE = 'http://opendata.peelregion.ca/media/25713/ward20102014_csv_12.2013.csv'
CHAIR_URL = 'https://www.peelregion.ca/council/councill/kolb.htm'

class PeelPersonScraper(Scraper): # @todo creates two people if that person represents two wards; instead, create two memberships as in ca_ab_grande_prairie_county_no_1

  def get_people(self):
    yield chair_info(CHAIR_URL)
    for row in csv_reader(COUNCIL_PAGE, header=True, headers={'Cookie': 'incap_ses_168_68279=7jCHCh608QQSFVti3dtUAviu/1IAAAAAIRf6OsZL0NttnlzANkVb6w=='}):

      p = Legislator(
        name='%(FirstName0)s %(LastName0)s' % row,
        post_id='%(MUNIC)s Ward %(WARDNUM)s' % row,
        role='Councillor',
      )
      p.add_contact('email', row['email0'], None)
      p.add_contact('voice', row['Phone0'], 'legislature')
      p.add_extra('boundary_url', '/boundaries/%s-wards/ward-%s/' % (row['MUNIC'].lower(), row['WARDNUM']))
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
        p.add_extra('boundary_url', '/boundaries/%s-wards/ward-%s/' % (row['MUNIC'].lower(), row['WARDNUM']))
        p.add_source(COUNCIL_PAGE)
        yield p

def chair_info(url):
  page = lxmlize(url)
  name = page.xpath('string(//title)').split('-')[1]
  photo_url = page.xpath('string(//div[@class="co-menu"]/img/@src)')
  # sadly, email is script-based
  address = page.xpath('string(//div[@id="co-content"]/p[1])').translate(
      None, '\r\t')
  phone = page.xpath(
      'string(//div[@id="co-content"]/p[2]/text())').split(':')[1]

  p = Legislator(name=name, post_id='Peel', role='Regional Chair',
                 image=photo_url)
  p.add_source(url)
  p.add_contact('address', address, 'legislature')
  p.add_contact('voice', phone, 'legislature')
  return p


