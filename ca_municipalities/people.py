from utils import CSVScraper, CanadianPerson as Person
from opencivicdata.divisions import Division
from pupa.scrape import Organization, Post
from collections import defaultdict

import re

LIST_PAGE = 'https://www.civicinfo.bc.ca/people'


class CanadaMunicipalitiesPersonScraper(CSVScraper):
    csv_url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQzUYBs5WnnMaFtdu6l98jPsJpTXR-mJqdRG6Beb02JMSmvq6FgZCGraBEUESuhEzNX8TDhqX2p1YM8/pub?output=csv'
    other_names = {}
    corrections = {}
    organizations = {}

    """
    Returns whether the row should be imported. By default, skips empty rows
    and rows in which a name component is "Vacant".
    """
    def is_valid_row(self, row):
        empty = ('', 'Vacant')
        if not any(row.values()):
            return False
        if 'first name' in row and 'last name' in row:
            return row['last name'] not in empty and row['first name'] not in empty
        return row['full name'] not in empty

    def scrape(self):
        seat_numbers = defaultdict(lambda: defaultdict(int))

        reader = self.csv_reader(self.csv_url, delimiter=self.delimiter, header=True, encoding=self.encoding, skip_rows=self.skip_rows)
        reader.fieldnames = [self.header_converter(field) for field in reader.fieldnames]
        for row in reader:

            if self.is_valid_row(row):
                for key, corrections in self.corrections.items():
                    if not isinstance(corrections, dict):
                        row[key] = corrections(row[key])
                    elif row[key] in corrections:
                        row[key] = corrections[row[key]]

                organizationClassification = row.get('classification')
                if not organizationClassification:
                    organizationClassification = 'government'

                organization = None
                organizationName = row['organization']
                if organizationName:
                    if self.organizations.get(organizationName.lower()):
                        organization = self.organizations.get(organizationName.lower())
                    else:
                        organization = Organization(organizationName, classification=organizationClassification)
                        organization.add_source(self.csv_url)
                        yield organization
                        self.organizations[organizationName] = organization
                else:
                    continue

                # ca_qc_laval: "maire et president du comite executif", "conseiller et membre du comite executif"
                # ca_qc_montreal: "Conseiller de la ville; Membre…", "Maire d'arrondissement\nMembre…"
                if row.get('primary role'):
                    row['primary role'] = re.split(r'(?: (?:et)\b|[;\n])', row['primary role'], 1)[0].strip()

                roleName = row.get('primary role')
                #division_id=parent.id,
                post = Post(role=roleName, label=organizationName, organization_id=organization._id)
                yield post


                name = row['full name']

                province = row.get('province')
                role = row['primary role']

                # ca_qc_laval: "maire …", "conseiller …"
                if role not in ('candidate', 'member') and not re.search(r'[A-Z]', role):
                    role = role.capitalize()

                if self.district_name_format_string:
                    if row['district id']:
                        district = self.district_name_format_string.format(**row)
                    else:
                        district = self.jurisdiction.division_name
                elif row.get('district name'):
                    district = row['district name']
                elif self.fallbacks.get('district name'):
                    district = row[self.fallbacks['district name']] or self.jurisdiction.division_name
                else:
                    district = self.jurisdiction.division_name

                district = district.replace('–', '—')  # n-dash, m-dash

                # ca_qc_montreal
                if district == 'Ville-Marie' and role == 'Maire de la Ville de Montréal':
                    district = self.jurisdiction.division_name

                if self.many_posts_per_area and role not in self.unique_roles:
                    seat_numbers[role][district] += 1
                    district = '{} (seat {})'.format(district, seat_numbers[role][district])

                p = Person(primary_org=organizationClassification, name=name, district=district, role=role, party=row.get('party name'))
                p.add_source(self.csv_url)

                if not row.get('district name') and row.get('district id'):  # ca_on_toronto_candidates
                    if len(row['district id']) == 7:
                        p._related[0].extras['boundary_url'] = '/boundaries/census-subdivisions/{}/'.format(row['district id'])

                if row.get('gender'):
                    p.gender = row['gender']
                if row.get('photo url'):
                    p.image = row['photo url']

                if row.get('source url'):
                    p.add_source(row['source url'])

                if row.get('website'):
                    p.add_link(row['website'], note='web site')
                if row.get('facebook'):
                    p.add_link(re.sub(r'[#?].+', '', row['facebook']))
                if row.get('twitter'):
                    p.add_link(row['twitter'])

                if row['email']:
                    p.add_contact('email', row['email'].strip().split('\n')[-1])  # ca_qc_montreal
                if row['address']:
                    p.add_contact('address', row['address'], 'legislature')
                if row.get('phone'):
                    p.add_contact('voice', row['phone'].split(';', 1)[0], 'legislature')  # ca_qc_montreal, ca_on_huron
                if row.get('fax'):
                    p.add_contact('fax', row['fax'], 'legislature')
                if row.get('cell'):
                    p.add_contact('cell', row['cell'], 'legislature')
                if row.get('birth date'):
                    p.birth_date = row['birth date']

                if row.get('incumbent'):
                    p.extras['incumbent'] = row['incumbent']

                if name in self.other_names:
                    for other_name in self.other_names[name]:
                        p.add_name(other_name)

                yield p