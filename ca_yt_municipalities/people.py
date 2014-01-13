from pupa.scrape import Scraper, Legislator
from pupa.models import Organization
from utils import lxmlize

import re
import urllib2
import os
import subprocess

COUNCIL_PAGE = 'http://www.community.gov.yk.ca/pdf/loc_govdir.pdf'


class YukonMunicipalitiesPersonScraper(Scraper):

  def get_people(self):
    response = urllib2.urlopen(COUNCIL_PAGE).read()
    pdf = open('/tmp/yt.pdf', 'w')
    pdf.write(response)
    pdf.close()

    data = subprocess.check_output(['pdftotext', '-layout', '/tmp/yt.pdf', '-'])
    data = re.split(r'\n\s*\n', data)
    for municipality in data:

      if not 'Councillors' in municipality:
        continue
      lines = municipality.split('\n')
      if 'Page' in lines[0]:
        lines.pop(0)
        if not lines[0].strip():
          lines.pop(0)
      col1end = re.search(r'\s{2,}(\w)', lines[0].strip()).end()
      col2end = re.search(r':\s{2,}(\w)', lines[0].strip()).end()

      if 'Council' in lines[1]:
        address = lines[2][:col1end - 1].strip() + ' ' + lines[3][:col1end - 1].strip()
        district = lines[0][:col1end - 1].strip() + ' ' + lines[1][:col1end - 1].strip()
      else:
        address = lines[1][:col1end - 1].strip() + ' ' + lines[2][:col1end - 1].strip()
        district = lines[0][:col1end - 1].strip()

      chamber = district + ' Council'
      organization = Organization(name=chamber, chamber=chamber, classification='legislature', jurisdiction_id=self.jurisdiction.jurisdiction_id)
      organization.add_source(COUNCIL_PAGE)
      yield organization

      phone = re.findall(r'(?<=Phone: )\(?(\d{3}[\)-] ?\d{3}-\d{4})', municipality)[0].replace(') ', '-')
      email = re.findall(r'(?<=E-mail:) (\S*)', municipality)[0]
      fax = None
      if 'Fax' in municipality:
        fax = re.findall(r'(?<=Fax: )\(?(\d{3}[\)-] ?\d{3}-\d{4})', municipality)[0].replace(') ', '-')
      website = None
      if 'Website' in municipality:
        website = re.findall(r'((http:\/\/|www.)(\S*))', municipality)[0][0]

      councillor_or_mayor = False
      for line in lines:
        if 'Mayor:' in line:
          councillor_or_mayor = True
          role = 'Mayor'
          continue
        if 'Councillors' in line:
          councillor_or_mayor = True
          role = 'Councillor'
          continue
        if councillor_or_mayor:
          councillor = line[col1end - 1:col2end - 1].strip()
          if not councillor:
            continue
          p = Legislator(name=councillor, post_id=district)
          p.add_source(COUNCIL_PAGE)
          p.add_membership(organization, role=role, chamber=chamber)
          p.add_contact('address', address, 'legislature')
          p.add_contact('voice', phone, 'legislature')
          p.add_contact('email', email, None)
          if fax:
            p.add_contact('fax', fax, 'legislature')
          if website:
            p.add_link(website, None)
          yield p

    os.system('rm yt.pdf')
