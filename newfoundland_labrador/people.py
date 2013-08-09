from pupa.scrape import Scraper, Legislator
from larvae.person import Person
from larvae.organization import Organization

from utils import lxmlize

import re, urllib2, os

COUNCIL_PAGE = 'http://www.ma.gov.nl.ca/ma/municipal_directory/index.html'

class Newfoundland_LabradorPersonScraper(Scraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)
    url = page.xpath('//a[contains(text(),"Municipal Directory")]/@href')[0]
    
    response = urllib2.urlopen(url).read()
    pdf = open('nl.pdf', 'w')
    pdf.write(response)
    pdf.close()

    os.system('pdftotext nl.pdf -layout')
    txt = open('nl.txt', 'r')
    pages = txt.read().split('Municipal Directory')[1:]
    for page in pages:
      page = page.splitlines(True)
      column_index = {}
      for line in page:
        if 'Official Name' in line:
          column_index['dist_end'] = re.search('Region', line).start()
          column_index['name_start'] = re.search('Mayor', line).start()+1
          column_index['name_end'] = re.search('Clerk', line).start()-1
          column_index['phone_start'] = re.search('Line 1', line).start()
          column_index['phone_end'] = re.search('Line 2', line).start()-1
          column_index['fax_start'] = re.search('Fax', line).start()
          column_index['fax_end'] = re.search('E-mail', line).start()-2
          column_index['email_start'] = column_index['fax_end']+1
          column_index['email_end'] = re.search('Address', line).start()-1
          column_index['address_start'] = column_index['email_end']+1
          column_index['address_end'] = re.search('Days', line).start()-1
          break
      for line in page:
        if 'Official Name' in line or not line.strip():
          continue
        district = line[:column_index['dist_end']]
        name = line[column_index['name_start']:column_index['name_end']].strip()
        phone = line[column_index['phone_start']:column_index['phone_end']].strip().replace('(','').replace(') ','-')
        fax = line[column_index['fax_start']:column_index['fax_end']].strip().replace('(','').replace(') ','-')
        email = line[column_index['email_start']:column_index['email_end']].strip()
        address = line[column_index['address_start']:column_index['address_end']].strip()
        address = re.sub(r'\s{2,}',', ', address)
        if not name or not district:
          continue
        p = Legislator(name=name, post_id=district)
        p.add_source(COUNCIL_PAGE)
        p.add_source(url)
        if phone:
          p.add_contact('phone', phone, None)
        # Im excluding fax because that column isn't properly aligned
        # if fax:
        #   p.add_contact('fax', fax, None)
        if email:
          p.add_contact('email', email, None)
        if address:
          p.add_contact('address', address, None)
        yield p
    os.system('rm nl.pdf')
    os.system('rm nl.txt')