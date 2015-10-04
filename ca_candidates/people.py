from __future__ import unicode_literals
from utils import CanadianScraper, CanadianPerson as Person, clean_string

import csv
import json
import math
import os
import re

import lxml.html
import requests
import scrapelib
from lxml import etree
from opencivicdata.divisions import Division
from pupa.utils import get_pseudo_id
from six import StringIO
from six.moves.urllib.parse import parse_qs, quote_plus, urlparse, urlsplit


class CanadaCandidatesPersonScraper(CanadianScraper):

    def scrape(self):
        # Get the candidates' incumbency.
        representatives = json.loads(self.get('http://represent.opennorth.ca/representatives/house-of-commons/?limit=0').text)['objects']
        self.incumbents = [representative['name'] for representative in representatives]

        # Needed to map the crowdsourced data.
        boundaries = json.loads(self.get('http://represent.opennorth.ca/boundaries/federal-electoral-districts-next-election/?limit=0').text)['objects']
        boundary_name_to_boundary_id = {boundary['name'].lower(): boundary['external_id'] for boundary in boundaries}

        # Get the crowdsourced data.
        crowdsourcing = {}
        response = self.get('https://docs.google.com/spreadsheets/d/1BNjqBeGDsjiGOtsAu2K5qR1a3Cq_1sfVoDH7mE1WFU0/export?gid=1338986395&format=csv')
        response.encoding = 'utf-8'
        for row in csv.DictReader(StringIO(response.text)):
            # Uniquely identify the candidate.
            boundary_id = row['District Number']
            if not re.search(r'\A\d{5}\Z', boundary_id):
                boundary_id = boundary_name_to_boundary_id[boundary_id.lower()]
            key = '{}/{}/{}'.format(row['Party name'], boundary_id, row['Name'])

            if crowdsourcing.get(key):
                self.warning('{} already exists'.format(key))
            else:
                if row['Gender'] == 'M':
                    gender = 'male'
                elif row['Gender'] == 'F':
                    gender = 'female'
                else:
                    gender = None

                crowdsourcing[key] = {
                    'gender': gender,
                    'email': row['Email'],
                    'image': row['Photo URL'],
                    'facebook': row['Facebook'],
                    'instagram': row['Instagram'],
                    'twitter': row['Twitter'],
                    'linkedin': row['LinkedIn'],
                    'youtube': row['YouTube'],
                    # XXX Website, Office type, Address, Phone, Fax
                }

        # Steps to merge the crowdsource data.
        steps = {
            'gender': (
                lambda p: p.gender,
                lambda p, value: setattr(p, 'gender', value),
            ),
            'email': (
                lambda p: next((contact_detail['value'] for contact_detail in p._related[0].contact_details if contact_detail['type'] == 'email'), None),
                lambda p, value: p.add_contact('email', value),
            ),
            'image': (
                lambda p: p.image,
                lambda p, value: setattr(p, 'image', value),
            ),
        }

        self.birth_date = 1900

        # Scrape each party separately. Unscraped parties with more than 10 candidates:
        # http://communist-party.ca/
        # http://www.eatgoogle.com/en/candidates/

        if os.environ.get('METHOD'):
            methods = os.environ.get('METHOD').split(',')
        else:
            methods = (
                'bloc_quebecois',
                'christian_heritage',
                'communist',
                'conservative',
                'forces_et_democratie',
                'green',
                'independent',
                'liberal',
                'libertarian',
                'marxist_leninist',
                'ndp',
                # Run last to fill in any missing slots.
                'elections_canada',
            )

        seen = {}
        scraped_parties = (
            'Bloc Québécois',
            'Christian Heritage',
            'Communist',
            'Conservative',
            'Forces et Démocratie',
            'Green Party',
            'Independent',
            'Liberal',
            'Libertarian',
            'Marxist–Leninist',
            'NDP',
        )

        for method in methods:
            for p in getattr(self, 'scrape_{}'.format(method))():
                if not p._related[0].post_id:
                    raise Exception('No post_id for {} of {}'.format(p.name, p._related[1].organization_id))

                # Uniquely identify the candidate.
                boundary_id = get_pseudo_id(p._related[0].post_id)['label']
                party = get_pseudo_id(p._related[1].organization_id)['name']
                if not re.search(r'\A\d{5}\Z', boundary_id):
                    try:
                        boundary_id = boundary_name_to_boundary_id[boundary_id.lower()]
                    except KeyError:
                        raise Exception("KeyError: '{}' on {}".format(boundary_id.lower(), method))
                key = '{}/{}/{}'.format(party, boundary_id, p.name)

                # Names from Elections Canada may differ, but there may also be
                # multiple independents per district.
                if party == 'Independent':
                    seen_key = key
                else:
                    seen_key = '{}/{}'.format(party, boundary_id)
                if seen.get(seen_key):
                    # We got the candidate from a scraper.
                    if method == 'elections_canada':
                        continue
                    # We got the same candidate from different scrapers.
                    else:
                        raise Exception('{} seen in {} during {}'.format(seen_key, seen[seen_key], method))
                elif method == 'elections_canada':
                    # We should have gotten the candidate from a scraper.
                    if party in scraped_parties:
                        if party == 'Independent':
                            self.error('{} not seen'.format(seen_key))
                        else:
                            self.warning('{} not seen'.format(seen_key))
                # We are getting the candidate from a scraper.
                else:
                    seen[seen_key] = method

                # Merge the crowdsourced data.
                if crowdsourcing.get(key):
                    o = crowdsourcing[key]

                    links = {}
                    for link in p.links:
                        domain = '.'.join(urlsplit(link['url']).netloc.split('.')[-2:])
                        if domain in ('facebook.com', 'fb.com'):
                            links['facebook'] = link['url']
                        elif domain == 'instagram.com':
                            links['instagram'] = link['url']
                        elif domain == 'linkedin.com':
                            links['linkedin'] = link['url']
                        elif domain == 'twitter.com':
                            links['twitter'] = link['url']
                        elif domain == 'youtube.com':
                            links['youtube'] = link['url']

                    for prop, (getter, setter) in steps.items():
                        if o[prop]:
                            if prop == 'email' and '.gc.ca' in o[prop]:
                                self.info('{}: skipping email = {}'.format(key, o[prop]))
                            else:
                                scraped = getter(p)
                                if not scraped:
                                    setter(p, o[prop])
                                    self.debug('{}: adding {} = {}'.format(key, prop, o[prop]))
                                elif scraped.lower() != o[prop].lower() and prop != 'image':
                                    self.warning('{}: expected {} to be {}, not {}'.format(key, prop, scraped, o[prop]))

                    for prop in ['facebook', 'instagram', 'linkedin', 'twitter', 'youtube']:
                        if o[prop]:
                            scraped = links.get(prop)
                            entered = re.sub(r'/timeline/\Z|\?(f?ref|lang|notif_t)=.+|\?_rdr\Z', '', o[prop].replace('@', '').replace('http://twitter.com/', 'https://twitter.com/'))  # Facebook, Twitter
                            if not scraped:
                                p.add_link(entered)
                                self.debug('{}: adding {} = {}'.format(key, prop, entered))
                            elif scraped.lower() != entered.lower():
                                self.warning('{}: expected {} to be {}, not {}'.format(key, prop, scraped, entered))

                yield p

    def scrape_bloc_quebecois(self):
        url = 'http://www.blocquebecois.org/candidats/'
        page = self.lxmlize(url)

        pages = math.ceil(int(re.search(r'\d+', page.xpath('//option[1]/text()')[0]).group(0)) / 10)
        pattern = 'http://www.blocquebecois.org/candidats/page/{}/'

        for page_number in range(1, pages + 1):
            if page_number > 1:
                page = self.lxmlize(pattern.format(page_number))

            nodes = page.xpath('//article')
            if not len(nodes):
                raise Exception('{} returns no candidates'.format(url))
            for node in nodes:
                district = node.xpath('.//h1/a/text()|.//div[@class="infos"]//a[1]/text()')

                if district:
                    name = ' '.join(node.xpath('.//h2/a/text()|.//div[@class="infos"]//a[2]/text()')).strip()
                    district = district[0].replace('–', '—').strip()  # n-dash, m-dash

                    if district in DIVISIONS_MAP:
                        district = DIVISIONS_MAP[district]

                    p = Person(primary_org='lower', name=name, district=district, role='candidate', party='Bloc Québécois')
                    if name == 'Jean-François Caron':
                        p.birth_date = str(self.birth_date)
                        self.birth_date += 1

                    p.image = node.xpath('./div[@class="image"]//@src')[0]

                    p.add_contact('email', node.xpath('.//@data-mail')[0].replace('!', '.').replace('%', '@'))

                    voice = self.get_phone(node, error=False)
                    if voice:
                        p.add_contact('voice', voice, 'office')

                    self.add_links(p, node)

                    if name in self.incumbents:
                        p.extras['incumbent'] = True

                    p.add_source(url)
                    yield p

    def scrape_christian_heritage(self):
        def char(code):
            try:
                return chr(int(code))
            except ValueError:
                return code

        url = 'https://www.chp.ca/candidates'

        nodes = self.lxmlize(url).xpath('//ul[@id="nav_cat_archive"]//li/a/@href[1]')
        if not len(nodes):
            raise Exception('{} returns no candidates'.format(url))
        for href in nodes:
            try:
                page = self.lxmlize(href)

                meta = page.xpath('//meta[@property="og:title"]/@content')[0].split(' - ')
                name = meta[0]
                district = page.xpath('//a[contains(@href,".pdf")]/@href')[0].rsplit('/', 1)[1][0:5]
                if not re.search(r'\A\d{5}\Z', district):
                    district = meta[1]

                p = Person(primary_org='lower', name=name, district=district, role='candidate', party='Christian Heritage')

                p.image = page.xpath('//meta[@property="og:image"]/@content')[0]

                voice = self.get_phone(page.xpath('//span[@class="phone"]')[0], error=False)
                if voice:
                    p.add_contact('voice', voice, 'office')

                script = page.xpath('//span[@class="email"]/script/text()')[0]
                codes = reversed(re.findall(r"[\[,]'(.+?)'", script))
                content = ''.join(char(code) for code in codes)
                p.add_contact('email', re.search(r'>E: (.+)<', content).group(1))

                p.add_source(href)
                yield p
            except requests.exceptions.ChunkedEncodingError:
                pass  # too bad for that candidate

    def scrape_communist(self):
        urls = self.lxmlize('http://communist-party.ca/').xpath('//aside[@id="text-16"]//@href')
        for url in urls:
            if url == 'http://communist-party.ca/east-coast':
                heading_level = 1
            else:
                heading_level = 2

            page = self.lxmlize(url)
            for empty in page.xpath('//h{}[not(.//text())]'.format(heading_level)):
                empty.getparent().remove(empty)

            nodes = page.xpath('//div[@id="content"]//h{}'.format(heading_level))
            if heading_level == 1:
                nodes = nodes[1:]
            if not len(nodes):
                raise Exception('{} returns no candidates'.format(url))
            for node in nodes:
                elements = node.xpath('./following-sibling::*')
                index = next((i for i, e in enumerate(elements) if e.tag == 'h{}'.format(heading_level)), None)
                if index:
                    elements = elements[:index]

                name = next((e.xpath('.//text()')[0] for e in elements if e.tag == 'h{}'.format(heading_level + 1)), None)
                district = node.xpath('.//text()')[0].strip().replace(' — ', '—').replace(' –', '—')  # m-dash, m-dash, n-dash

                if district in DIVISIONS_MAP:
                    district = DIVISIONS_MAP[district]
                elif district == 'London':
                    district = 'London West'

                p = Person(primary_org='lower', name=name, district=district, role='candidate', party='Communist')
                image = next((e.xpath('.//img[contains(@class,"size-thumbnail")]/@src')[0] for e in elements if e.tag in ('h3', 'p') and e.xpath('.//@src')), None)
                if image:
                    p.image = image
                else:
                    raise Exception('expected image {}'.format(url))

                details = next((e for e in elements if e.tag == 'h6'), None)
                if details is not None:
                    link = details.xpath('.//@href')
                    if link:
                        p.add_link(link[0])
                    else:
                        link = details.xpath('.//text()')[0].lower()
                        if 'communist-party.ca' not in link:
                            link = details.getprevious().xpath('.//text()')[0].lower()
                        if 'communist-party.ca' in link:
                            p.add_link('http://' + link)
                    p.add_contact('email', next((re.sub(r' ?\[at\] ?', '@', clean_string(text)) for text in details.xpath('.//text()') if '[at]' in text), None))
                    p.add_contact('voice', self.get_phone(details), 'office')
                else:
                    detail_url = next((e.xpath('.//span[contains(@id,"read_moregtgt")]//@href')[0] for e in reversed(elements) if e.tag == 'h3'), None)
                    if not detail_url:
                        detail_url = next((e.xpath('.//@href')[0] for e in elements if e.tag == 'p' and e.xpath('.//@href')), None)
                    p.add_link(detail_url)

                    page = self.lxmlize(detail_url)
                    content = page.xpath('//div[@id="content"]')
                    if content:
                        voice = self.get_phone(content[0], error=False)
                        if voice:
                            p.add_contact('voice', voice, 'office')
                        email = self.get_email(content[0], error=False)
                        if not email:
                            email = next((clean_string(text).replace(' [at] ', '@') for text in content[0].xpath('.//text()') if '[at]' in text), None)
                        p.add_contact('email', email)
                    else:
                        self.warning('no details for {}'.format(detail_url))

                p.add_source(url)
                yield p

    def scrape_conservative(self):
        url = 'http://www.conservative.ca/?member=candidates'
        user_agent = 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)'
        doc = lxml.html.fromstring(json.loads(self.get(url, headers={'User-Agent': user_agent}).text))

        nodes = doc.xpath('//a[contains(@class,"team-list-person-block")]')
        if not len(nodes):
            raise Exception('{} returns no candidates'.format(url))
        for node in nodes:
            name = node.attrib['data-name'].strip()
            district = node.attrib['data-title']
            if district in DIVISIONS_MAP:
                district = DIVISIONS_MAP[district]
            else:
                district = re.sub(r'\bî', 'Î', district).replace(' ', ' ').strip()  # non-breaking space
                district = district.replace('--', '—')  # m-dash
                district = district.replace(' – ', '—')  # n-dash, m-dash
                district = district.replace('–', '—')  # n-dash, m-dash
                district = district.replace('―', '—')  # horizontal bar, m-dash

            if district in DIVISIONS_MAP:
                district = DIVISIONS_MAP[district]

            p = Person(primary_org='lower', name=name, district=district, role='candidate', party='Conservative')
            if name == 'Robert Kitchen':
                p.birth_date = str(self.birth_date)
                self.birth_date += 1

            if node.attrib['data-image'] != '/media/team/no-image.jpg':
                p.image = 'https://represent-image-proxy.herokuapp.com/{}/150/150'.format(quote_plus('http://www.conservative.ca{}'.format(node.attrib['data-image'])))

            if node.attrib['data-website'] not in ('www.conservateur.ca', 'www.conservative.ca'):
                p.add_link('http://{}'.format(node.attrib['data-website']))

            if node.attrib['data-facebook'] != 'cpcpcc':
                p.add_link('https://www.facebook.com/{}'.format(re.sub(r'\?f?ref=.+', '', node.attrib['data-facebook'])))

            twitter = node.attrib['data-twitter']
            if twitter not in ('pcc_hq', 'cpc_hq'):
                twitter = twitter.replace('@', '')
                # @note Remove once corrected.
                if twitter == 'DavidAnderson89':
                    twitter = 'DavidAndersonSK'
                elif twitter == 'MPJoeDaniel':
                    twitter = 'joedanielcpc'
                elif twitter == 'MinRonaAmbrose':
                    twitter = 'RonaAmbrose'
                p.add_link('https://twitter.com/{}'.format(twitter))

            email = node.attrib['data-email']
            if email and email not in ('info@conservative.ca', 'info@conservateur.ca', 'www.reelectandrewscheer.ca'):
                p.add_contact('email', email)

            detail_url = 'http://www.conservative.ca/team/{}'.format(node.attrib['data-learn'])

            try:
                page = self.lxmlize(detail_url)

                span = page.xpath('//div[@class="aside-text-address"]')
                if span:
                    voice = self.get_phone(span[0], error=False)
                    if voice:
                        p.add_contact('voice', voice, 'office')

                # @note If the above email disappears, use this.
                # span = page.xpath('//span[@class="__cf_email__"]/@data-cfemail')
                # if span:
                #     code = span[0]
                #     operand = int(code[:2], 16)
                #     email = ''.join(chr(int(code[i:i + 2], 16) ^ operand) for i in range(2, len(code), 2))
                #     p.add_contact('email', email)
            except scrapelib.HTTPError:
                pass  # 404

            if name in self.incumbents:
                p.extras['incumbent'] = True

            p.add_link(detail_url)
            p.add_source(url)
            yield p

    def scrape_elections_canada(self):
        parties = {
            'Alliance of the North': 'Alliance of the North',
            'Animal Alliance Environment Voters Party of Canada': 'Animal Alliance Environment Voters',
            'Bloc Québécois': 'Bloc Québécois',
            'Canada Party': 'Canada',
            'Canadian Action Party': 'Canadian Action',
            'Christian Heritage Party of Canada': 'Christian Heritage',
            'Conservative Party of Canada': 'Conservative',
            'Communist Party of Canada': 'Communist',
            'Democratic Advancement Party of Canada': 'Democratic Advancement',
            'Green Party of Canada': 'Green Party',
            'Forces et Démocratie': 'Forces et Démocratie',
            'Independent': 'Independent',
            'Liberal Party of Canada': 'Liberal',
            'Libertarian Party of Canada': 'Libertarian',
            'Marijuana Party': 'Marijuana',
            'Marxist-Leninist Party of Canada': 'Marxist–Leninist',
            'New Democratic Party': 'NDP',
            'No Affiliation': 'Independent',
            'Party for Accountability, Competency and Transparency': 'Party for Accountability, Competency and Transparency',
            'Pirate Party of Canada': 'Pirate',
            'Progressive Canadian Party': 'Progressive Canadian',
            'Rhinoceros Party': 'Rhinoceros',
            'Seniors Party of Canada': 'Seniors',
            'The Bridge Party of Canada': 'Bridge',
            'United Party of Canada': 'United',
        }

        for division in Division.get('ocd-division/country:ca').children('ed'):
            if division.attrs['validFrom'] == '2015-10-19':
                district = division.id.rsplit(':', 1)[1].replace('-2013', '')

                url = 'http://www.elections.ca/Scripts/vis/candidates?L=e&EV=41&PAGEID=17&ED={}'.format(district)
                response = requests.get(url)

                nodes = lxml.html.fromstring(response.text).xpath('//table//tr[position()>1]')
                if not len(nodes):
                    raise Exception('{} returns no candidates'.format(url))
                for node in nodes:
                    name = re.sub(r'\s+', ' ', node.xpath('./td[1]/text()')[0].strip().replace("''", '"'))
                    party = parties[node.xpath('./td[3]/text()')[0].strip()]

                    p = Person(primary_org='lower', name=name, district=district, role='candidate', party=party)

                    voice = node.xpath('./td[4]/text()')[0].strip()
                    if voice and voice != '0':
                        p.add_contact('voice', voice, 'office')

                    if name in self.incumbents and (name != 'Scott Andrews' or district == '10001'):
                        p.extras['incumbent'] = True

                    p.add_source(url)
                    yield p

    def scrape_forces_et_democratie(self):
        url = 'http://www.forcesetdemocratie.org/l-equipe/candidats.html'
        user_agent = 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)'

        nodes = self.lxmlize(url, user_agent=user_agent).xpath('//ul[@class="liste-candidats"]/li')
        if not len(nodes):
            raise Exception('{} returns no candidates'.format(url))
        for node in nodes:
            link = node.xpath('./a/@href')[0]

            name = node.xpath('./h4/text()')[0]
            district = self.lxmlize(link, user_agent=user_agent).xpath('//span[@class="txt-vert"]/text()')

            if district:
                p = Person(primary_org='lower', name=name, district=district[0], role='candidate', party='Forces et Démocratie')

                image = node.xpath('.//img/@src')[0]
                if 'forceetdemocratie1_-_F_-_couleur_-_HR.jpg' not in image:
                    p.image = image

                p.add_link(link)
                self.add_links(p, node)

                if name in self.incumbents:
                    p.extras['incumbent'] = True

                p.add_source(url)
                yield p

    def scrape_green(self):
        url = 'http://www.greenparty.ca/en/candidates'

        nodes = self.lxmlize(url).xpath('//div[contains(@class,"candidate-card")]')
        if not len(nodes):
            raise Exception('{} returns no candidates'.format(url))
        for node in nodes:
            name = node.xpath('.//div[@class="candidate-name"]//text()')[0]
            district = node.xpath('.//@data-target')[0][5:]  # node.xpath('.//div[@class="riding-name"]//text()')[0]

            if name == name.lower():
                name = name.title()
            elif re.search(r'\b[a-z]', name):
                name = ' '.join(component.title() for component in name.split(' '))

            p = Person(primary_org='lower', name=name, district=district, role='candidate', party='Green Party')
            detail_url = node.xpath('.//div/@data-src')[0]
            try:
                image = lxml.html.fromstring(detail_url).xpath('//@src')[0]  # print quality also available
                if '.png' not in image:
                    p.image = image
            except lxml.etree.XMLSyntaxError:
                self.warning('lxml.etree.XMLSyntaxError on {}'.format(detail_url))

            p.add_contact('email', self.get_email(node))

            link = node.xpath('.//div[@class="margin-bottom-gutter"]/a[contains(@href,"http")]/@href')
            if link:
                p.add_link(link[0])
            self.add_links(p, node)

            if name in self.incumbents:
                p.extras['incumbent'] = True

            p.add_source(url)
            yield p

    def scrape_independent(self):
        p = Person(primary_org='lower', name='Scott Andrews', district='10001', role='candidate', party='Independent')
        p.image = 'http://www.scottandrews.ca/Images/photo_scott.jpg'
        p.add_contact('voice', '709-631-2355', 'office')
        p.extras['incumbent'] = True
        p.add_source('http://www.scottandrews.ca/campaign/default.aspx')
        p.birth_date = str(self.birth_date)
        self.birth_date += 1
        yield p

        p = Person(primary_org='lower', name='James Ford', district='48032', role='candidate', party='Independent')
        p.image = 'http://jamesfordindependent.ca/jamesfordindependent.ca/HOME_files/PastedGraphic-2.jpg'
        p.add_contact('email', 'info@jamesfordindependent.ca')
        p.add_contact('voice', '587-990-2061', 'office')
        p.add_source('http://jamesfordindependent.ca/')
        yield p

        p = Person(primary_org='lower', name='Brent Rathgeber', district='48031', role='candidate', party='Independent')
        p.image = 'http://brentrathgeber.com/wordpress/wp-content/uploads/2015/08/CLA-photo.jpg'
        p.add_contact('voice', '780-460-1018', 'office')
        p.add_contact('fax', '780-460-7205', 'office')
        p.add_contact('email', 'reelectbrent@gmail.com')
        p.add_link('https://www.facebook.com/Re-Elect-Brent-Rathgeber-for-St-Albert-Edmonton-156806981046354')
        p.add_link('https://www.youtube.com/user/BrentRathgberMP')
        p.add_link('https://twitter.com/brentrathgeber')
        p.extras['incumbent'] = True
        p.add_source('http://brentrathgeber.com/')
        yield p

        url = 'http://www.punditsguide.ca/new/inc/get_future_elec_details_tbl.php?party=10'
        district = None

        name_corrections = {
            'Christopher Lloyd': 'Chris Lloyd',
            'Cliff Williams': 'Clifford James Williams',
            'Hector Daniel Clouthier': 'Hector Clouthier',
            'John C. Turner': 'John Clayton Turner',
            'Kelvin Chicago-Boucher': 'Kelvin Boucher-Chicago',
        }

        nodes = self.lxmlize(url).xpath('//tbody/tr')[1:]
        if not len(nodes):
            raise Exception('{} returns no candidates'.format(url))
        for node in nodes:
            offset = node.xpath('./td[1]/@colspan')

            if offset:
                # Use same district as previous row.
                offset = int(offset[0]) - 1
            else:
                district = node.xpath('./td[2]/a/text()')[0]
                offset = 0

            name = node.xpath('./td[{}]/a/text()'.format(8 - offset))[0]
            name = ' '.join(re.sub(r' \([^)]+\)', '', clean_string(name)).split(', ')[::-1]).lower()
            name = ' '.join(re.sub(r'(\b(?:mac)?)([a-z])', lambda s: s.group(1).title() + s.group(2).title(), component) for component in name.split(' '))

            if name in ('Scott Andrews', 'James Ford', 'Brent M. Rathgeber'):
                continue
            # Conform to Elections Canada.
            elif name in name_corrections:
                name = name_corrections[name]

            p = Person(primary_org='lower', name=name, district=district, role='candidate', party='Independent')
            if name == 'Jean-François Caron':
                p.birth_date = str(self.birth_date)
                self.birth_date += 1

            gender = clean_string(node.xpath('./td[{}]'.format(6 - offset)))
            if gender == 'F':
                p.gender = 'female'
            elif gender == 'M':
                p.gender = 'male'

            link = node.xpath('./td[{}]/a/@href'.format(9 - offset))
            if link:
                p.add_link(link[0])

            p.add_source(url)
            yield p

    def scrape_liberal(self):
        url = 'https://www.liberal.ca/candidates/'
        cookies = {'YPF8827340282Jdskjhfiw_928937459182JAX666': json.loads(self.get('http://ipinfo.io/json').text)['ip']}

        nodes = self.lxmlize(url, cookies=cookies).xpath('//ul[@id="candidates"]/li')
        if not len(nodes):
            raise Exception('{} returns no candidates'.format(url))
        for node in nodes:
            name = node.xpath('./h2/text()')[0]
            district = node.xpath('./@data-riding-riding_id')[0]  # node.xpath('./@data-riding-name')[0]

            # @note Remove once corrected.
            if name == 'Nicola Di lorio':
                name = 'Nicola Di Iorio'

            p = Person(primary_org='lower', name=name, district=district, role='candidate', party='Liberal')
            p.image = node.xpath('./@data-photo-url')[0][4:-1]

            # @note Remove once corrected.
            if name in ('Carla Qualtrough', 'Cynthia Block', 'Ginette Petitpas Taylor', 'Karley Scott', 'Lisa Abbott', 'Liz Riley', 'Rebecca Chartrand'):
                p.gender = 'female'
            elif node.xpath('./@class[contains(.,"candidate-female")]'):
                p.gender = 'female'
            elif node.xpath('./@class[contains(.,"candidate-male")]'):
                p.gender = 'male'

            link = node.xpath('.//a[substring(@href,string-length(@href)-11)=".liberal.ca/"]/@href|.//a[substring(@href,string-length(@href)-10)=".liberal.ca"]/@href')
            self.add_links(p, node)

            if link:
                try:
                    # http://susanwatt.liberal.ca/ redirects to http://www.liberal.ca/
                    sidebar = self.lxmlize(link[0].replace('www.', ''), cookies=cookies).xpath('//div[@id="sidebar"]')
                    if sidebar:
                        email = self.get_email(sidebar[0], error=False)
                        if email:
                            p.add_contact('email', email)
                        voice = self.get_phone(sidebar[0], error=False)
                        if voice:
                            p.add_contact('voice', voice, 'office')

                        p.add_link(link[0])
                except (requests.exceptions.ConnectionError, scrapelib.HTTPError):
                    pass

            if name in self.incumbents:
                p.extras['incumbent'] = True

            p.add_source(url)
            yield p

    def scrape_libertarian(self):
        url = 'https://www.libertarian.ca/candidates/'

        nodes = self.lxmlize(url).xpath('//div[contains(@class,"tshowcase-inner-box")]')
        if not len(nodes):
            raise Exception('{} returns no candidates'.format(url))
        for node in nodes:
            name = node.xpath('.//div[@class="tshowcase-box-title"]//text()')
            if name:
                district = node.xpath('.//div[@class="tshowcase-single-position"]//text()')
                if district:
                    district = district[0].replace('- ', '—').replace(' – ', '—').replace('–', '—').replace('\u200f', '').strip()  # hyphen, n-dash, n-dash, RTL mark
                else:
                    district = 'TBD'  # will be skipped

                if district in DIVISIONS_MAP:
                    district = DIVISIONS_MAP[district]
                elif district == 'Selkirk-Interlake':
                    district = 'Selkirk—Interlake—Eastman'

                if district != 'TBD':
                    p = Person(primary_org='lower', name=name[0], district=district, role='candidate', party='Libertarian')

                    image = node.xpath('.//div[contains(@class,"tshowcase-box-photo")]//img/@src')[0]
                    if 'default.png' not in image:
                        p.image = image

                    sidebar = self.lxmlize(node.xpath('.//a/@href')[0]).xpath('//div[@class="tshowcase-single-email"]')
                    if sidebar:
                        p.add_contact('email', self.get_email(sidebar[0]))
                    else:
                        email = node.xpath('.//a[./i[contains(@class,"fa-envelope-o")]]/@href')
                        if email:
                            p.add_contact('email', re.sub(r'mailto: ?', '', email[0].replace(url, '')))

                    self.add_links(p, node)

                    p.add_source(url)
                    yield p

    def scrape_marxist_leninist(self):
        url = 'http://mlpc.ca/2015/candidates-for-the-marxist-leninist-party-of-canada/'
        user_agent = 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)'

        nodes = self.lxmlize(url, user_agent=user_agent).xpath('//div[@class="fl-rich-text"][.//img[contains(@class,"candidate-box")]]')
        if not len(nodes):
            raise Exception('{} returns no candidates'.format(url))
        for node in nodes:
            name = node.xpath('.//strong/text()')[0]
            district = ''.join(clean_string(text) for text in node.xpath('.//em/text()'))

            if district in DIVISIONS_MAP:
                district = DIVISIONS_MAP[district]

            p = Person(primary_org='lower', name=name, district=district, role='candidate', party='Marxist–Leninist')
            p.image = node.xpath('.//img[contains(@class,"candidate-box")]/@src')[0]

            p.add_source(url)
            yield p

    def scrape_ndp(self):
        # @note Switch to using https://docs.google.com/spreadsheets/d/11suA7-cjo1KH_WtCquQ3IMIzhvzyW3SVNa56iVGEGAY/pub?gid=1264102253&single=true&output=csv

        payload = {
            # sheet, min row, max row, min col, max col
            'ranges': '[null,[[null,"1264102253",1,338,0,26]]]',
        }

        emails = {}
        response = self.post('https://docs.google.com/spreadsheets/d/11suA7-cjo1KH_WtCquQ3IMIzhvzyW3SVNa56iVGEGAY/fetchrows', data=payload)
        cells = json.loads(response.text[5:])['perGridRangeSnapshots'][0]['snapshot'][0][-1][-1]
        for i in range(0, len(cells), 26):
            # If the email column is not None and has a value:
            if cells[i + 3][3] and cells[i + 3][3][-1]:
                emails[int(cells[i][3][-1])] = cells[i + 3][3][-1].replace(' ', '')

        url = 'http://www.ndp.ca/team'

        nodes = self.lxmlize(url, encoding='utf-8').xpath('//div[contains(@class,"candidate-holder ")]')[1:]
        if not len(nodes):
            raise Exception('{} returns no candidates'.format(url))
        for node in nodes:
            image = node.xpath('.//@data-img')[0]

            name = node.xpath('.//div[@class="candidate-name"]//text()')[0]
            district = re.search(r'\d{5}', image).group(0)  # node.xpath('.//span[@class="candidate-riding-name"]/text()')[0]

            p = Person(primary_org='lower', name=name, district=district, role='candidate', party='NDP')
            if name in ('Erin Weir', 'Robert Kitchen', 'Scott Andrews'):
                p.birth_date = str(self.birth_date)
                self.birth_date += 1

            p.image = image

            if node.xpath('.//div[contains(@class,"placeholder-f")]'):
                p.gender = 'female'
            elif node.xpath('.//div[contains(@class,"placeholder-m")]'):
                p.gender = 'male'

            twitter = node.xpath('.//a[@class="candidate-twitter"]/@href')
            if twitter:
                p.add_link(twitter[0])
            facebook = node.xpath('.//a[@class="candidate-facebook"]/@href')
            if facebook:
                # @note Remove once corrected.
                if 'www.ndp.ca' in facebook[0]:
                    facebook[0] = facebook[0].replace('www.ndp.ca', 'www.facebook.com')
                elif facebook[0] == 'https://fb.com/DraftJennyKwan2015':
                    facebook[0] = 'https://www.facebook.com/JennyKwanVanEast'
                p.add_link(facebook[0])

            email = None
            link = node.xpath('.//a[@class="candidate-website"]/@href')
            if link:
                p.add_link(link[0])

                try:
                    node = self.lxmlize(link[0]).xpath('//div[@class="contact-phone"]')
                    if node:
                        email = self.get_email(node[0], error=False)
                        if email:
                            p.add_contact('email', email)

                        voice = self.get_phone(node[0], error=False)
                        if voice:
                            p.add_contact('voice', voice, 'office')
                except etree.XMLSyntaxError:
                    self.warning('lxml.etree.XMLSyntaxError on {}'.format(link[0]))

            if not email and emails.get(int(district)):
                p.add_contact('email', emails[int(district)])

            if name in self.incumbents and name != 'Scott Andrews':
                p.extras['incumbent'] = True

            p.add_source(url)
            yield p

    def add_links(self, p, node):
        for substring in ('facebook.com', 'fb.com', 'instagram.com', 'linkedin.com', 'twitter.com', 'youtube.com'):
            link = self.get_link(node, substring, error=False)
            if link:
                if link[:3] == 'ttp':
                    link = 'h' + link
                elif 'facebook.com' in link and 'twitter.com' in link:
                    link = parse_qs(urlparse(link).query)['u'][0]
                elif 'facebook.com' in link:
                    link = re.sub(r'/timeline/\Z|\?(?:f?ref|notif_t)=.+', '', link)
                elif 'twitter.com' in link:
                    link = re.sub(r'\?lang=fr\Z', '', link.replace('@', ''))
                    if link.startswith('http://'):
                        link = link.replace('http://twitter.com/', 'https://twitter.com/')
                p.add_link(link)

DIVISIONS_MAP = {
    # Typo.
    "Courtney-Alberni": "Courtenay—Alberni",
    "Grand Prairie MacKenzie": "Grande Prairie—Mackenzie",
    "Hamilton East-Stony Creek": "Hamilton East—Stoney Creek",
    "Honor---Mercier": "Honoré-Mercier",
    "North Burnaby—Seymour": "Burnaby North—Seymour",
    "North Okangan-Shuswap": "North Okanagan—Shuswap",
    "Ottawa Ouest-Nepean": "Ottawa West—Nepean",
    "Pakdale-High Park": "Parkdale—High Park",
    "Richmond": "Richmond Centre",
    "Rosement―La Petite-Patrie": "Rosemont—La Petite-Patrie",
    "Sault-Sainte-Marie": "Sault Ste. Marie",
    "Surrey Center": "Surrey Centre",
    "Ville-Marie―Le Sud-Ouest―île-des-Sœurs": "Ville-Marie—Le Sud-Ouest—Île-des-Soeurs",
    "Ville-Marie—Le sud-ouest—Île-des-sœurs": "Ville-Marie—Le Sud-Ouest—Île-des-Soeurs",
    'Ville-Marie—Le Sud-Ouest—Île-des-Sœurs': "Ville-Marie—Le Sud-Ouest—Île-des-Soeurs",
    "Ville-Marie―Le Sud-Ouest―Îles-des-Soeurs": "Ville-Marie—Le Sud-Ouest—Île-des-Soeurs",
    "West Vancouver-Sunshine Coast-Sea to Sky County": "West Vancouver—Sunshine Coast—Sea to Sky Country",
    "West Vancouver - Sunshine Coast - Sea to Sky County": "West Vancouver—Sunshine Coast—Sea to Sky Country",
    # Mix of hyphens, m-dashes and/or spaces.
    "Barrie-Springwater-Oro-Medonte": "Barrie—Springwater—Oro-Medonte",  # last hyphen remains a hyphen
    "Brossard-Saint Lambert": "Brossard—Saint-Lambert",
    "Chatham-Kent-Leamington": "Chatham-Kent—Leamington",  # first hyphen remains a hyphen
    "Laval-Les-Îles": "Laval—Les Îles",  # last hyphen becomes a space
    "Laurier–Sainte Marie": "Laurier—Sainte-Marie",
    "Mission-Matsqui - Fraser Canyon": "Mission—Matsqui—Fraser Canyon",
    "Saint-Maurice-Champlain": "Saint-Maurice—Champlain", # last hyphen becomes m-dash
}

for division in Division.get('ocd-division/country:ca').children('ed'):
    if division.attrs.get('validFrom') == '2015-10-19':
        DIVISIONS_MAP[division.name.lower()] = division.name
        if division.attrs['name_fr'] and division.attrs['name_fr'] != division.name:
            DIVISIONS_MAP[division.attrs['name_fr']] = division.name
        if ' ' in division.name:
            DIVISIONS_MAP[division.name.replace(' ', '-')] = division.name  # incorrect hyphen
        if '-' in division.name:  # hyphen
            DIVISIONS_MAP[division.name.replace('-', ' ')] = division.name  # incorrect space
        if '—' in division.name:  # m-dash
            DIVISIONS_MAP[division.name.replace('—', ' ')] = division.name  # incorrect space
            DIVISIONS_MAP[division.name.replace('—', '-')] = division.name  # incorrect hyphen
            DIVISIONS_MAP[division.name.replace('—', '–')] = division.name  # incorrect n-dash
