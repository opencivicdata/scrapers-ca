from __future__ import unicode_literals
from utils import CanadianScraper, CanadianPerson as Person

import re
import os
import subprocess

from pupa.scrape import Organization
from six.moves.urllib.request import urlopen

COUNCIL_PAGE = 'http://www.unsm.ca/doc_download/880-mayor-list-2013'


class NovaScotiaMunicipalitiesPersonScraper(CanadianScraper):

    def scrape(self):
        response = urlopen(COUNCIL_PAGE).read()
        pdf = open('/tmp/ns.pdf', 'w')
        pdf.write(response)
        pdf.close()

        data = subprocess.check_output(['pdftotext', '/tmp/ns.pdf', '-'])
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

            org = Organization(name=district + ' Municipal Council', classification='legislature', jurisdiction_id=self.jurisdiction.jurisdiction_id)
            org.add_source(COUNCIL_PAGE)
            yield org

            p = Person(primary_org='legislature', name=name, district=district)
            p.add_source(COUNCIL_PAGE)
            membership = p.add_membership(org, role='Mayor', district=district)

            address = lines.pop(0).strip() + ', ' + lines.pop(0).strip()
            if 'Phone' not in lines[0]:
                address = address + ', ' + lines.pop(0).strip()

            if 'Phone' not in lines[0]:
                address = address + ', ' + lines.pop(0).strip()

            phone = lines.pop(0).split(':')[1].strip()
            if 'Fax' in lines.pop(0):
                fax = lines.pop(0)

            membership.add_contact_detail('address', address, 'legislature')
            membership.add_contact_detail('voice', phone, 'legislature')
            membership.add_contact_detail('fax', fax, 'legislature')
            # @todo emails are being assigned incorrectly, e.g. Town of Berwick picks
            # up Cape Breton Regional Municipality and Region of Queens Municipality
            for i, email in enumerate(emails):
                regex = name.split()[-1].lower() + '|' + '|'.join(district.split()[-2:]).replace('of', '').lower()
                regex = regex.replace('||', '|')
                matches = re.findall(r'{}'.format(regex), email)
                if matches:
                    membership.add_contact_detail('email', emails.pop(i))
            yield p

        os.system('rm /tmp/ns.pdf')
