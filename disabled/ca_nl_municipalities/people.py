from __future__ import unicode_literals
from utils import CanadianScraper, CanadianPerson as Person
from pupa.scrape import Organization

import os
import re
import subprocess
from urllib.request import urlopen

COUNCIL_PAGE = 'http://www.ma.gov.nl.ca/ma/municipal_directory/index.html'


class NewfoundlandAndLabradorMunicipalitiesPersonScraper(CanadianScraper):

    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)
        url = page.xpath('//a[contains(text(),"Municipal Directory")]/@href')[0]

        response = urlopen(url).read()
        pdf = open('/tmp/nl.pdf', 'w')
        pdf.write(response)
        pdf.close()

        data = subprocess.check_output(['pdftotext', '-layout', '/tmp/nl.pdf', '-'])
        pages = data.split('Municipal Directory')[1:]
        for page in pages:
            page = page.splitlines(True)
            column_index = {}
            for line in page:
                if 'Official Name' in line:
                    column_index['dist_end'] = re.search('Region', line).start()
                    column_index['name_start'] = re.search('Mayor', line).start() + 1
                    column_index['name_end'] = re.search('Clerk', line).start() - 1
                    column_index['phone_start'] = re.search('Line 1', line).start()
                    column_index['phone_end'] = re.search('Line 2', line).start() - 1
                    column_index['fax_start'] = re.search('Fax', line).start()
                    column_index['fax_end'] = re.search('E-mail', line).start() - 2
                    column_index['email_start'] = column_index['fax_end'] + 1
                    column_index['email_end'] = re.search('Address', line).start() - 1
                    column_index['address_start'] = column_index['email_end'] + 1
                    column_index['address_end'] = re.search('Days', line).start() - 1
                    break
            for line in page:
                if 'Official Name' in line or not line.strip():
                    continue
                district = line[:column_index['dist_end']]
                name = line[column_index['name_start']:column_index['name_end']].strip()
                phone = line[column_index['phone_start']:column_index['phone_end']].strip().replace('(', '').replace(') ', '-')
                # fax = line[column_index['fax_start']:column_index['fax_end']].strip().replace('(', '').replace(') ', '-')
                email = line[column_index['email_start']:column_index['email_end']].strip()
                address = line[column_index['address_start']:column_index['address_end']].strip()
                address = re.sub(r'\s{2,}', ', ', address)
                if not name or not district:
                    continue

                org = Organization(name=district + ' Municipal Council', classification='legislature', jurisdiction_id=self.jurisdiction.jurisdiction_id)
                org.add_source(COUNCIL_PAGE)
                org.add_source(url)
                yield org

                p = Person(primary_org='legislature', name=name, district=district)
                p.add_source(COUNCIL_PAGE)
                p.add_source(url)
                membership = p.add_membership(org, role='Mayor', district=district)
                if phone:
                    membership.add_contact_detail('voice', phone, 'legislature')
                # I'm excluding fax because that column isn't properly aligned
                # if fax:
                #   membership.add_contact_detail('fax', fax)
                if email:
                    membership.add_contact_detail('email', email)
                if address:
                    membership.add_contact_detail('address', address, 'legislature')
                yield p
        os.system('rm /tmp/nl.pdf')
