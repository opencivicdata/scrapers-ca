# coding: utf-8
from __future__ import unicode_literals

import csv
import re
from collections import defaultdict
from ftplib import FTP

import lxml.html
import requests
from lxml import etree
from opencivicdata.divisions import Division
from pupa.scrape import Scraper, Jurisdiction, Organization, Person
from six import StringIO, string_types, text_type
from six.moves.urllib.parse import urlparse, unquote

import patch  # patch patches validictory # noqa

CONTACT_DETAIL_TYPE_MAP = {
    'Address': 'address',
    'bb': 'cell',  # BlackBerry
    'bus': 'voice',
    'Bus': 'voice',
    'Bus.': 'voice',
    'Business': 'voice',
    'Cell': 'cell',
    'Cell Phone': 'cell',
    'Email': 'email',
    'Fax': 'fax',
    'Home': 'voice',
    'Home Phone': 'voice',
    'Home Phone*': 'voice',
    'Office': 'voice',
    'ph': 'voice',
    'Phone': 'voice',
    'Res': 'voice',
    'Res/Bus': 'voice',
    'Residence': 'voice',
    'Téléphone (bureau)': 'voice',
    'Téléphone (cellulaire)': 'cell',
    'Téléphone (résidence)': 'voice',
    'Téléphone (résidence et bureau)': 'voice',
    'Voice Mail': 'voice',
    'Work': 'voice',
}
# In Newmarket, for example, there are both "Phone" and "Business" numbers.
CONTACT_DETAIL_NOTE_MAP = {
    'Address': 'legislature',
    'bb': 'legislature',
    'bus': 'office',
    'Bus': 'office',
    'Bus.': 'office',
    'Business': 'office',
    'Cell': 'legislature',
    'Cell Phone': 'legislature',
    'Email': None,
    'Fax': 'legislature',
    'Home': 'residence',
    'Home Phone': 'residence',
    'Home Phone*': 'residence',
    'ph': 'legislature',
    'Phone': 'legislature',
    'Office': 'legislature',
    'Res': 'residence',
    'Res/Bus': 'office',
    'Residence': 'residence',
    'Téléphone (bureau)': 'legislature',
    'Téléphone (cellulaire)': 'legislature',
    'Téléphone (résidence)': 'residence',
    'Téléphone (résidence et bureau)': 'legislature',
    'Voice Mail': 'legislature',
    'Work': 'legislature',
}

email_re = re.compile(r'([A-Za-z0-9._-]+@(?:[A-Za-z0-9-]+\.)+[A-Za-z]{2,})')


styles_of_address = {}
for gid in range(3):
    response = requests.get('https://docs.google.com/spreadsheet/pub?key=0AtzgYYy0ZABtdFJrVTdaV1h5XzRpTkxBdVROX3FNelE&single=true&gid=%d&output=csv' % gid)
    response.encoding = 'utf-8'
    for row in csv.DictReader(StringIO(response.text)):
        identifier = row.pop('Identifier')
        for field in list(row.keys()):
            if not row[field] or field == 'Name':
                row.pop(field)
        if row:
            styles_of_address[identifier] = row


class CanadianScraper(Scraper):

    def get_email(self, node, expression='.', *, error=True):

        """
        Make sure that the node/expression is narrow enough to not capture a
        generic email address in the footer of the page, for example.
        """

        matches = []
        # If the text would be split across multiple sub-tags.
        for match in node.xpath('{}//*[contains(text(), "@")]'.format(expression)):
            matches.append(match.text_content())
        # The text version is more likely to be correct, as it is more visible,
        # e.g. ca_bc has one `href` of `mailto:first.last.mla@leg.bc.ca`.
        for match in node.xpath('{}//a[contains(@href,"mailto:")]'.format(expression)):
            matches.append(unquote(match.attrib['href']))
        # If the node has no sub-tags.
        if not matches:
            for match in node.xpath('{}//text()[contains(., "@")]'.format(expression)):
                matches.append(match)
        if matches:
            for match in matches:
                match = email_re.search(match)
                if match:
                    return match.group(1)
            if error:
                raise Exception('No email pattern in %s' % matches)
        elif error:
            raise Exception('No email node in %s' % etree.tostring(node))

    def get_phone(self, node, area_codes, *, error=True):

        """
        Don't use if multiple telephone numbers are present, e.g. voice and fax.
        If writing a new scraper, check that extensions are captured.
        """
        match = node.xpath('.//a[contains(@href,"tel:")]')
        if match:
            return match[0].attrib['href'].replace('tel:', '')
        for area_code in area_codes:
            match = re.search(r'(?:\A|\D)(\(?%d\)?\D?\d{3}\D?\d{4}(?:\s*(?:/|x|ext[.:]?|poste)[\s-]?\d+)?)(?:\D|\Z)' % area_code, node.text_content())
            if match:
                return match.group(1)
        if error:
            raise Exception('No phone pattern')

    def lxmlize(self, url, encoding='utf-8', user_agent=requests.utils.default_user_agent()):
        self.user_agent = user_agent

        entry = self.urlopen(url)
        if encoding != 'utf-8' or not isinstance(entry, text_type):
            entry = entry.encode(encoding)

        page = lxml.html.fromstring(entry)
        meta = page.xpath('//meta[@http-equiv="refresh"]')
        if meta:
            _, url = meta[0].attrib['content'].split('=', 1)
            return self.lxmlize(url, encoding)
        else:
            page.make_links_absolute(url)
            return page

    def csv_reader(self, url, header=False, encoding=None, skip_rows=0, **kwargs):
        result = urlparse(url)
        if result.scheme == 'ftp':
            data = StringIO()
            ftp = FTP(result.hostname)
            ftp.login(result.username, result.password)
            ftp.retrbinary('RETR %s' % result.path, lambda block: data.write(block.decode('utf-8')))
            ftp.quit()
            data.seek(0)
        else:
            response = self.get(url, **kwargs)
            if encoding:
                response.encoding = encoding
            data = StringIO(response.text.strip())
        if skip_rows:
            for _ in range(skip_rows):
                data.readline()
        if header:
            return csv.DictReader(data)
        else:
            return csv.reader(data)


class CSVScraper(CanadianScraper):
    encoding = None
    many_posts_per_area = False
    skip_rows = 0

    def scrape(self):
        seat_numbers = defaultdict(lambda: defaultdict(int))

        reader = self.csv_reader(self.csv_url, header=True, encoding=self.encoding, skip_rows=self.skip_rows)
        reader.fieldnames = [capitalize(field) for field in reader.fieldnames]
        for row in reader:
            if any(row.values()):
                district = row.get('District name') or self.jurisdiction.division_name
                role = row['Primary role']
                name = '%s %s' % (row['First name'], row['Last name'])
                province = row.get('Province')

                if role == 'Town Councillor':  # Oakville
                    role = 'Councillor'
                if province == 'Ontario':  # Guelph
                    province = 'ON'

                if self.many_posts_per_area and role != 'Mayor':
                    seat_numbers[role][district] += 1
                    district = '%s (seat %d)' % (district, seat_numbers[role][district])

                lines = []
                if row.get('Address line 1'):
                    lines.append(row['Address line 1'])
                if row.get('Address line 2'):
                    lines.append(row['Address line 2'])
                parts = [row['Locality']]
                if province:
                    parts.append(province)
                if row.get('Postal code'):
                    parts.extend(['', row['Postal code']])
                lines.append(' '.join(parts))

                p = CanadianPerson(primary_org='legislature', name=name, district=district, role=role)
                p.add_source(self.csv_url)
                if row.get('Gender'):
                    p.gender = row['Gender']
                if row['Photo URL']:
                    p.image = row['Photo URL']
                if row['Source URL']:
                    p.add_source(row['Source URL'])
                if row.get('Website'):
                    p.add_link(row['Website'])
                p.add_contact('email', row['Email'])
                p.add_contact('address', '\n'.join(lines), 'legislature')
                p.add_contact('voice', row['Phone'], 'legislature')
                if row.get('Fax'):
                    p.add_contact('fax', row['Fax'], 'legislature')
                if row.get('Cell'):
                    p.add_contact('cell', row['Cell'], 'legislature')
                elif row.get('Phone (cell)'):  # Oakville
                    p.add_contact('cell', row['Phone (cell)'], 'legislature')
                elif row.get('Phone (mobile)'):  # Guelph
                    p.add_contact('cell', row['Phone (mobile)'], 'legislature')
                if row.get('Facebook'):
                    p.add_link(re.sub(r'[#?].+', '', row['Facebook']))
                if row.get('Twitter'):
                    p.add_link(row['Twitter'])
                yield p


class CanadianJurisdiction(Jurisdiction):

    def __init__(self):
        super(CanadianJurisdiction, self).__init__()
        for module, name in (('people', 'Person'),):
            class_name = self.__class__.__name__ + name + 'Scraper'
            self.scrapers[module] = getattr(__import__(self.__module__ + '.' + module, fromlist=[class_name]), class_name)

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)

        parent = Division.get(self.division_id)
        if parent._type not in ('province', 'territory'):
            organization.add_post(role=styles_of_address[self.division_id]['Leader'], label=parent.name)

        children = [child for child in parent.children() if child._type != 'place']

        for child in children:
            if child:
                if getattr(self, 'use_type_id', False):
                    label = child.id.rsplit('/', 1)[1].capitalize().replace(':', ' ')
                else:
                    label = child.name
                organization.add_post(role=styles_of_address[self.division_id]['Member'], label=label)

        if not children and parent.attrs['posts_count']:
            for i in range(1, int(parent.attrs['posts_count'])):  # exclude Mayor
                organization.add_post(role=styles_of_address[self.division_id]['Member'], label='%s (seat %d)' % (parent.name, i))

        yield organization


class CanadianPerson(Person):

    def __init__(self, *, name, district, role, **kwargs):
        name = clean_name(name)
        district = clean_string(district).replace('&', 'and')
        role = clean_string(role)
        if role == 'City Councillor':
            role = 'Councillor'
        for k, v in kwargs.items():
            if isinstance(v, string_types):
                kwargs[k] = clean_string(v)
        super(CanadianPerson, self).__init__(name=name, district=district, role=role, **kwargs)

    def __setattr__(self, name, value):
        if name == 'gender':
            if value == 'M':
                value = 'male'
            elif value == 'F':
                value = 'female'
        super(CanadianPerson, self).__setattr__(name, value)

    def add_link(self, url, *, note=''):
        if url.startswith('www.'):
            url = 'http://%s' % url
        if re.match(r'\A@[A-Za-z]+\Z', url):
            url = 'https://twitter.com/%s' % url[1:]

        self.links.append({'note': note, 'url': url})

    # @todo Over time, we should replace all calls to `add_contact` with calls to
    # `add_contact_detail` on a Membership. We will have to override Membership's
    # `add_contact_detail` method to tidy the values.
    def add_contact(self, type, value, note='', area_code=None):
        if type:
            type = clean_string(type)
        if note:
            note = clean_string(note)
        if type in CONTACT_DETAIL_TYPE_MAP:
            type = CONTACT_DETAIL_TYPE_MAP[type]
        if note in CONTACT_DETAIL_NOTE_MAP:
            note = CONTACT_DETAIL_NOTE_MAP[note]

        type = type.lower()

        if type in ('text', 'voice', 'fax', 'cell', 'video', 'pager'):
            value = self.clean_telephone_number(clean_string(value), area_code=area_code)
        elif type == 'address':
            value = self.clean_address(value)
        else:
            value = clean_string(value)

        # The post membership is added before the party membership.
        self._related[0].add_contact_detail(type=type, value=value, note=note)

    def clean_telephone_number(self, s, area_code=None):
        """
        @see http://www.noslangues-ourlanguages.gc.ca/bien-well/fra-eng/typographie-typography/telephone-eng.html
        """

        splits = re.split(r'(?:/|x|ext[.:]?|poste)[\s-]?(?=\b|\d)', s, flags=re.IGNORECASE)
        digits = re.sub(r'\D', '', splits[0])

        if len(digits) == 7 and area_code:
            digits = '1' + str(area_code) + digits
        elif len(digits) == 10:
            digits = '1' + digits

        if len(digits) == 11 and digits[0] == '1' and len(splits) <= 2:
            digits = re.sub(r'\A(\d)(\d{3})(\d{3})(\d{4})\Z', r'\1-\2-\3-\4', digits)
            if len(splits) == 2:
                return '%s x%s' % (digits, splits[1])
            else:
                return digits
        else:
            return s

    def clean_address(self, s):
        """
        Corrects the postal code, abbreviates the province or territory name, and
        formats the last line of the address.
        """

        # The letter "O" instead of the numeral "0" is a common mistake.
        s = re.sub(r'\b[A-Z][O0-9][A-Z]\s?[O0-9][A-Z][O0-9]\b', lambda x: x.group(0).replace('O', '0'), clean_string(s))
        for k, v in abbreviations.items():
            s = re.sub(r'[,\n ]+\(?' + k + r'\)?(?=(?:[,\n ]+Canada)?(?:[,\n ]+[A-Z][0-9][A-Z]\s?[0-9][A-Z][0-9])?\Z)', ' ' + v, s)
        return re.sub(r'[,\n ]+([A-Z]{2})(?:[,\n ]+Canada)?[,\n ]+([A-Z][0-9][A-Z])\s?([0-9][A-Z][0-9])\Z', r' \1  \2 \3', s)


whitespace_re = re.compile(r'\s+', flags=re.U)
whitespace_and_newline_re = re.compile(r'[^\S\n]+', flags=re.U)
honorific_prefix_re = re.compile(r'\A(?:Councillor|Dr|Hon|M|Mayor|Mme|Mr|Mrs|Ms|Miss)\.? ')
honorific_suffix_re = re.compile(r', Ph\.D\Z')
capitalize_re = re.compile(r' [A-Z](?=[a-z])')  # to not lowercase "URL"

table = {
    ord('​'): ' ',  # zero-width space
    ord('’'): "'",
    ord('\xc2'): " ",  # non-breaking space if mixing ISO-8869-1 into UTF-8
}

# @see https://github.com/opencivicdata/ocd-division-ids/blob/master/identifiers/country-ca/ca_provinces_and_territories.csv
# @see https://github.com/opencivicdata/ocd-division-ids/blob/master/identifiers/country-ca/ca_provinces_and_territories-name_fr.csv
abbreviations = {
    'Newfoundland and Labrador': 'NL',
    'Prince Edward Island': 'PE',
    'Nova Scotia': 'NS',
    'New Brunswick': 'NB',
    'Québec': 'QC',
    'Ontario': 'ON',
    'Manitoba': 'MB',
    'Saskatchewan': 'SK',
    'Alberta': 'AB',
    'British Columbia': 'BC',
    'Yukon': 'YT',
    'Northwest Territories': 'NT',
    'Nunavut': 'NU',

    'PEI': 'PE',
}


def clean_string(s):
    return re.sub(r' *\n *', '\n', whitespace_and_newline_re.sub(' ', text_type(s).translate(table)).strip())


def clean_name(s):
    return honorific_suffix_re.sub('', honorific_prefix_re.sub('', whitespace_re.sub(' ', text_type(s).translate(table)).strip()))


def capitalize(s):
    return capitalize_re.sub(lambda s: s.group(0).lower(), s.strip())
