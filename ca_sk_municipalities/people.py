from pupa.scrape import Scraper
from pupa.models import Organization

from utils import lxmlize, Legislator

import re
import urllib2
import os
import subprocess

COUNCIL_PAGE = 'http://www.municipal.gov.sk.ca/Programs-Services/Municipal-Directory-pdf'
# See also HTML format http://www.mds.gov.sk.ca/apps/Pub/MDS/welcome.aspx


class SaskatchewanMunicipalitiesPersonScraper(Scraper):

  def get_people(self):
    response = urllib2.urlopen(COUNCIL_PAGE).read()
    pdf = open('/tmp/sk.pdf', 'w')
    pdf.write(response)
    pdf.close()

    data = subprocess.check_output(['pdftotext', '-layout', '/tmp/sk.pdf', '-'])

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
        index = index.end() - 1
      else:
        index = -1
      dist1 = []
      dist2 = []
      for line in page:
        dist1.append(line[:index].strip())
        dist2.append(line[index:].strip())
      districts.append(dist1)
      districts.append(dist2)

    for district in districts:

      district_name = district.pop(0).split(',')[0].title()

      chamber = district_name + ' Council'
      org = Organization(name=chamber, chamber=chamber, classification='legislature', jurisdiction_id=self.jurisdiction.jurisdiction_id)
      org.add_source(COUNCIL_PAGE)

      councillors = []
      contacts = {}
      for i, line in enumerate(district):
        if 'Phone' in line:
          phone = line.split(':')[1].replace('(', '').replace(') ', '-').strip()
          if phone:
            contacts['voice'] = phone
        if 'Fax' in line:
          fax = line.split(':')[1].replace('(', '').replace(') ', '-').strip()
          if fax:
            contacts['fax'] = fax
        if 'E-Mail' in line:
          email = line.split(':')[1].strip()
          if email:
            contacts['email'] = email
        if 'Address' in line and line.split(':')[1].strip():
          address = line.split(':')[1].strip() + ', ' + ', '.join(district[i + 1:]).replace(' ,', '')
          contacts['address'] = address
        if 'Mayor' in line or 'Councillor' in line or 'Alderman' in line:
          councillor = line.split(':')[1].replace('Mr.', '').replace('Mrs.', '').replace('Ms.', '').replace('His Worship', '').replace('Her Worship', '').strip()
          role = line.split(':')[0].strip()
          if councillor:
            councillors.append([councillor, role])

      if not councillors:
        continue
      yield org
      for councillor in councillors:
        p = Legislator(name=councillor[0], post_id=district_name, chamber=chamber)
        p.add_source(COUNCIL_PAGE)
        membership = p.add_membership(org, role=councillor[1], post_id=district_name, chamber=chamber)

        for key, value in contacts.iteritems():
          membership.add_contact_detail(key, value, None if key == 'email' else 'legislature')
        yield p
    os.system('rm /tmp/sk.pdf')
