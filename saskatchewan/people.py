from pupa.scrape import Scraper, Legislator
from larvae.person import Person
from larvae.organization import Organization

from utils import lxmlize

import re, urllib2, os

COUNCIL_PAGE = 'http://www.municipal.gov.sk.ca/Programs-Services/Municipal-Directory-pdf'

class SaskatchewanPersonScraper(Scraper):

  def get_people(self):
    response = urllib2.urlopen(COUNCIL_PAGE).read()
    pdf = open('sk.pdf', 'w')
    pdf.write(response)
    pdf.close()

    os.system('pdftotext sk.pdf -layout')
    txt = open('sk.txt', 'r')
    data = txt.read()

    data = data.splitlines(True)
    pages = []
    page = []
    for line in data:
      if line.strip() and not 'Page' in line and not 'CITIES' in line and not 'NORTHERN TOWNS, VILLAGES' in line:
        page.append(line)
      elif page:
        pages.append(page)
        page = []

    districts = []
    for page in pages:
      index = re.search(r'(\s{6,})', page[0])
      if index:
        index = index.end()-1
      else:
        index = -1
      dist1=[]
      dist2=[]
      for line in page:
        dist1.append(line[:index].strip())
        dist2.append(line[index:].strip())
      districts.append(dist1)
      districts.append(dist2)

    for district in districts:
      district_name = district.pop(0).split(',')[0].lower()
      councillors = []
      contacts = {}
      for i, line in enumerate(district):
        if 'Phone' in line:
          phone = line.split(':')[1].replace('(','').replace(') ', '-').strip()
          if phone:
            contacts['phone'] = phone
        if 'Fax' in line:
          fax = line.split(':')[1].replace('(','').replace(') ', '-').strip()
          if fax:
            contacts['fax'] = fax
        if 'E-Mail' in line:
          email = line.split(':')[1].strip()
          if email:
            contacts['email'] = email
        if 'Address' in line and line.split(':')[1].strip():
          address = line.split(':')[1].strip() + ', ' + ', '.join(district[i+1:]).replace(' ,','')
          contacts['address'] = address
        if 'Mayor' in line or 'Councillor' in line or 'Alderman' in line:
          councillor = line.split(':')[1].replace('Mr.','').replace('Mrs.','').replace('Ms.','').replace('His Worship','').replace('Her Worship','').strip()
          if councillor:
            councillors.append(councillor)
      
      for councillor in councillors:
        p = Legislator(district=district_name, name=councillor)
        p.add_source(COUNCIL_PAGE)
        for key, value in contacts.iteritems():
          p.add_contact(key, value, None)
        yield p
    os.system('rm sk.pdf')
    os.system('rm sk.txt')
