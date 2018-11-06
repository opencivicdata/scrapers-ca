from utils import CanadianScraper, CanadianPerson as Person
from opencivicdata.divisions import Division
from pupa.scrape import Organization

from collections import defaultdict
from datetime import date

COUNCIL_PAGE = 'https://docs.google.com/spreadsheets/d/1KHp2o8UzBhuYYYxdv4viFAPV6mZZwMSSK7f3Q43xy9k/pub?gid=400954018&single=true&output=csv'


class BritishColumbiaMunicipalitiesPersonScraper(CanadianScraper):
    updated_at = date(2016, 11, 8)
    contact_person = 'andrew@newmode.net'

    def scrape(self):
        exclude_divisions = {
            'ocd-division/country:ca/csd:5909052',  # Abbotsford
            'ocd-division/country:ca/csd:5915001',  # Langley (DM)
            'ocd-division/country:ca/csd:5915004',  # Surrey
            'ocd-division/country:ca/csd:5915015',  # Richmond
            'ocd-division/country:ca/csd:5915022',  # Vancouver
            'ocd-division/country:ca/csd:5915025',  # Burnaby
            'ocd-division/country:ca/csd:5915034',  # Coquitlam
            'ocd-division/country:ca/csd:5917021',  # Saanich
            'ocd-division/country:ca/csd:5917034',  # Victoria
            'ocd-division/country:ca/csd:5935010',  # Kelowna
        }
        expected_roles = {
            'Mayor',
            'Councillor',
        }
        unique_roles = {
            'Mayor',
        }
        infixes = {
            'CY': 'City',
            'DM': 'District',
            'IGD': 'District',
            'IM': 'Municipal',
            'RGM': 'Regional',
            'T': 'Town',
            'VL': 'Village',
        }
        duplicate_names = {
            'Colleen Evans',
        }

        names_to_ids = {}
        for division in Division.get('ocd-division/country:ca').children('csd'):
            type_id = division.id.rsplit(':', 1)[1]
            if type_id.startswith('59'):
                if division.attrs['classification'] == 'IRI':
                    continue
                if division.name in names_to_ids:
                    names_to_ids[division.name] = None
                else:
                    names_to_ids[division.name] = division.id

        reader = self.csv_reader(COUNCIL_PAGE, header=True)
        reader.fieldnames = [field.lower() for field in reader.fieldnames]

        organizations = {}
        seat_numbers = defaultdict(int)

        birth_date = 1900
        seen = set()

        rows = [row for row in reader]
        assert len(rows), 'No councillors found'
        for row in rows:
            name = row['full name']

            if not any(row.values()) or 'vacant' in name.lower():
                continue

            if row['district id']:
                division_id = 'ocd-division/country:ca/csd:{}'.format(row['district id'])
            else:
                division_id = names_to_ids[row['district name']]

            if division_id in exclude_divisions:
                continue
            if not division_id:
                raise Exception('unhandled collision: {}'.format(row['district name']))

            division = Division.get(division_id)

            division_name = division.name
            organization_name = '{} {} Council'.format(division_name, infixes[division.attrs['classification']])

            if division_id not in seen:
                seen.add(division_id)
                organizations[division_id] = Organization(name=organization_name, classification='government')
                organizations[division_id].add_source(COUNCIL_PAGE)

            organization = organizations[division_id]

            role = row['primary role']
            if role not in expected_roles:
                raise Exception('unexpected role: {}'.format(role))

            if role in unique_roles:
                district = division_name
            else:
                seat_numbers[division_id] += 1
                district = '{} (seat {})'.format(division_name, seat_numbers[division_id])
            if row['district id']:
                district += ' ({})'.format(division_id)

            organization.add_post(role=role, label=district, division_id=division_id)

            p = Person(primary_org='government', primary_org_name=organization_name, name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)
            if row['source url']:
                p.add_source(row['source url'])

            if name in duplicate_names:
                p.birth_date = str(birth_date)
                birth_date += 1

            p.add_contact('email', row['email'])
            p.add_contact('voice', row['phone'], 'legislature')

            p._related[0].extras['boundary_url'] = '/boundaries/census-subdivisions/{}/'.format(division_id.rsplit(':', 1)[1])

            yield p

        for organization in organizations.values():
            yield organization
