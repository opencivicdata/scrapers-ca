from pupa.scrape import Scraper, Legislator
from pupa.models import Organization
from utils import lxmlize, CanadianScraper

import re
import urllib2
import os
import subprocess

COUNCIL_PAGE = 'http://www.unsm.ca/doc_download/880-mayor-list-2013'


class NovaScotiaMunicipalitiesPersonScraper(CanadianScraper):

  def get_people(self):
    response = urllib2.urlopen(COUNCIL_PAGE).read()
    pdf = open('ns.pdf', 'w')
    pdf.write(response)
    pdf.close()

    data = subprocess.check_output(['pdftotext', 'ns.pdf', '-'])
    emails = re.findall(r'(?<=E-mail: ).+', data)
    data = re.split(r'Mayor |Warden ', data)[1:]
    for i, mayor in enumerate(data):
      lines = mayor.splitlines(True)
      name = lines.pop(0).strip()
      if name == "Jim Smith":
        continue
      district = lines.pop(0).strip()
      if not re.findall(r'[0-9]', lines[0]):
        district = district + ' ' + lines.pop(0).strip()

      chamber = district + ' Municipal Council'
      org = Organization(name=chamber, chamber=chamber, classification='legislature', jurisdiction_id=self.jurisdiction.jurisdiction_id)
      org.add_source(COUNCIL_PAGE)
      yield org

      p = Legislator(name=name, post_id=district)
      p.add_source(COUNCIL_PAGE)
      p.add_membership(org, role='Mayor', chamber=chamber)

      address = lines.pop(0).strip() + ', ' + lines.pop(0).strip()
      if not 'Phone' in lines[0]:
        address = address + ', ' + lines.pop(0).strip()

      if not 'Phone' in lines[0]:
        address = address + ', ' + lines.pop(0).strip()

      phone = lines.pop(0).split(':')[1].strip()
      if 'Fax' in lines.pop(0):
        fax = lines.pop(0)

      p.add_contact('address', address, 'legislature')
      p.add_contact('voice', phone, 'legislature')
      p.add_contact('fax', fax, 'legislature')
      # @todo emails are being assigned incorrectly, e.g. Town of Berwick picks
      # up Cape Breton Regional Municipality and Region of Queens Municipality
      for i, email in enumerate(emails):
        regex = name.split()[-1].lower() + '|' + '|'.join(district.split()[-2:]).replace('of', '').lower()
        regex = regex.replace('||', '|')
        matches = re.findall(r'%s' % regex, email)
        if matches:
          p.add_contact('email', emails.pop(i), None)
      yield p

    os.system('rm ns.pdf')
