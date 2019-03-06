from utils import CanadianScraper, CanadianPerson as Person
from opencivicdata.divisions import Division
from pupa.scrape import Organization
from datetime import date

COUNCIL_PAGE = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vR4i0tdtPJxFSXAccxZ1rjl8aIT-HApNcFs7In-thJJeLi4rKkXZMxIXkF1W0h_tK58QBgb3TZiEjQG/pub?output=csv'

class AlbertaCandidatesPersonScraper(CanadianScraper):
    updated_at = date(2019, 3, 6)
    contact_person = 'andrew@newmode.net'

    def scrape(self):
        exclude_divisions = {
        }
        exclude_districts = {
        }
        expected_roles = {
            'candidate',
        }
        infixes = {
            'CY': 'City',
            'DM': 'District',
            'IGD': 'District',
            'IM': 'Municipal',
            'RGM': 'Regional',
            'T': 'Town',
            'VL': 'Village',
            'RDA': 'District',
        }
        duplicate_names = {
        }

        names_to_ids = {}
        for division in Division.get('ocd-division/country:ca/province:ab').children('ed'):
            print(division)
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

        birth_date = 1900
        seen = set()

        rows = [row for row in reader]
        assert len(rows), 'No councillors found'
        for row in rows:
            name = row['name']
            district_name = row['district name']

            if not any(row.values()) or name.lower() in ('', 'vacant') or district_name in exclude_districts:
                continue

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

            district = division_name

            organization.add_post(role=role, label=district, division_id=division_id)

            p = Person(primary_org='government', primary_org_name=organization_name, name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)
            if row['source url']:
                p.add_source(row['source url'])

            if name in duplicate_names:
                p.birth_date = str(birth_date)
                birth_date += 1

            if row['email']:
                p.add_contact('email', row['email'])

            if row['phone']:
                p.add_contact('voice', row['phone'], 'legislature')

            if row['twitter']:
                p.add_link(row['twitter'])

            p._related[0].extras['boundary_url'] = '/boundaries/census-subdivisions/{}/'.format(division_id.rsplit(':', 1)[1])

            yield p

        for organization in organizations.values():
            yield organization
