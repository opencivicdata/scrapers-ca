from __future__ import unicode_literals
from utils import CanadianScraper, CanadianPerson as Person

import csv
import json
import math
import re

import lxml.html
import requests
import scrapelib
from pupa.utils import get_pseudo_id
from six import StringIO
from six.moves.urllib.parse import parse_qs, urlparse, urlsplit

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
        response = self.get('https://docs.google.com/spreadsheets/d/1BNjqBeGDsjiGOtsAu2K5qR1a3Cq_1sfVoDH7mE1WFU0/export?gid=368528247&format=csv')
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

        # Scrape each party separately.
        # @todo Pirate https://my.pirateparty.ca/election2015.html
        # @todo Rhinoceros http://www.eatgoogle.com/en/candidates/
        methods = (
            'bloc_quebecois',
            'christian_heritage',
            'conservative',
            'forces_et_democratie',
            'green',
            'liberal',
            'libertarian',
            'ndp',
        )
        for method in methods:
            for p in getattr(self, 'scrape_{}'.format(method))():
                # Uniquely identify the candidate.
                boundary_id = get_pseudo_id(p._related[0].post_id)['label']
                if not re.search(r'\A\d{5}\Z', boundary_id):
                    try:
                        boundary_id = boundary_name_to_boundary_id[boundary_id.lower()]
                    except KeyError:
                        raise Exception("KeyError: '{}' on {}".format(boundary_id.lower(), method))
                key = '{}/{}/{}'.format(get_pseudo_id(p._related[1].organization_id)['name'], boundary_id, p.name)

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
                            entered = re.sub(r'\?f?ref=.+|\?_rdr\Z', '', o[prop].replace('@', '').replace('http://twitter.com/', 'https://twitter.com/'))  # Facebook, Twitter
                            if not scraped:
                                p.add_link(entered)
                                self.debug('{}: adding {} = {}'.format(key, prop, entered))
                            elif scraped.lower() != entered.lower():
                                self.warning('{}: expected {} to be {}, not {}'.format(key, prop, scraped, entered))

                yield p

    def scrape_bloc_quebecois(self):
        url = 'http://www.blocquebecois.org/candidats/'

        pages = math.ceil(int(re.search(r'\d+', self.lxmlize(url).xpath('//option[1]/text()')[0]).group(0)) / 10)

        pattern = 'http://www.blocquebecois.org/candidats/page/{}/'

        for page in range(1, pages + 1):
            for node in self.lxmlize(pattern.format(page)).xpath('//article'):
                district = node.xpath('.//h1/text()')

                if district:
                    name = ' '.join(node.xpath('.//h2/text()'))
                    district = district[0].replace('–', '—')  # n-dash, m-dash

                    if district in DIVISIONS_MAP:
                        district = DIVISIONS_MAP[district]

                    p = Person(primary_org='lower', name=name, district=district, role='candidate', party='Bloc Québécois')

                    image = node.xpath('./div[@class="image"]/img/@src')
                    if image:
                        p.image = image[0]

                    email = self.get_email(node, error=False)
                    if email:
                        p.add_contact('email', email)

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
        for href in self.lxmlize(url).xpath('//ul[@id="nav_cat_archive"]//li/a/@href[1]'):
            page = self.lxmlize(href)

            name = page.xpath('//meta[@property="og:title"]/@content')[0].split(' - ')[0]
            district = page.xpath('//a[contains(@href,".pdf")]/@href')[0].rsplit('/', 1)[1][0:5]

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

    def scrape_conservative(self):
        url = 'http://www.conservative.ca/?member=candidates'
        doc = lxml.html.fromstring(json.loads(self.get(url).text))
        for node in doc.xpath('//a[contains(@class,"team-list-person-block")]'):
            name = node.attrib['data-name'].strip()
            district = node.attrib['data-title']
            if district in DIVISIONS_MAP:
                district = DIVISIONS_MAP[district]
            else:
                district = re.sub(r'\bî', 'Î', district).replace('--', '—').replace(' – ', '—').replace('–', '—').replace('―', '—').replace(' ', ' ').strip()  # m-dash, n-dash -> m-dash, n-dash -> m-dash, horizontal bar -> m-dash, non-breaking space

            if district in DIVISIONS_MAP:
                district = DIVISIONS_MAP[district]
            elif district in DIVISIONS_M_DASH:
                district = district.replace('-', '—')  # hyphen, m-dash

            p = Person(primary_org='lower', name=name, district=district, role='candidate', party='Conservative')
            if node.attrib['data-image'] != '/media/team/no-image.jpg':
                p.image = 'http://www.conservative.ca{}'.format(node.attrib['data-image'])

            if node.attrib['data-website'] != 'www.conservative.ca':
                p.add_link('http://{}'.format(node.attrib['data-website']))

            if node.attrib['data-facebook'] != 'cpcpcc':
                p.add_link('https://www.facebook.com/{}'.format(re.sub(r'\?f?ref=.+', '', node.attrib['data-facebook'])))

            twitter = node.attrib['data-twitter']
            if twitter != 'cpc_hq':
                # @note Remove once corrected.
                if twitter == 'DavidAnderson89':
                    twitter = 'DavidAndersonSK'
                elif twitter == 'MPJoeDaniel':
                    twitter = 'joedanielcpc'
                elif twitter == 'MinRonaAmbrose':
                    twitter = 'RonaAmbrose'
                p.add_link('https://twitter.com/{}'.format(node.attrib['data-twitter']))

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

    def scrape_forces_et_democratie(self):
        url = 'http://www.forcesetdemocratie.org/l-equipe/candidats.html'
        user_agent = 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)'
        for node in self.lxmlize(url, user_agent=user_agent).xpath('//ul[@class="liste-candidats"]/li'):
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
        for node in self.lxmlize(url).xpath('//div[contains(@class,"candidate-card")]'):
            name = node.xpath('.//div[@class="candidate-name"]//text()')[0].replace('Mark & Jan', 'Mark')
            district = node.xpath('.//@data-target')[0][5:]  # node.xpath('.//div[@class="riding-name"]//text()')[0]

            p = Person(primary_org='lower', name=name, district=district, role='candidate', party='Green Party')
            image = lxml.html.fromstring(node.xpath('.//div/@data-src')[0]).xpath('//@src')[0]  # print quality also available
            if '.png' not in image:
                p.image = image

            p.add_contact('email', self.get_email(node))

            link = node.xpath('.//div[@class="margin-bottom-gutter"]/a[contains(@href,"http")]/@href')
            if link:
                p.add_link(link[0])
            self.add_links(p, node)

            if name in self.incumbents:
                p.extras['incumbent'] = True

            p.add_source(url)
            yield p

    def scrape_liberal(self):
        url = 'https://www.liberal.ca/candidates/'
        cookies = {'YPF8827340282Jdskjhfiw_928937459182JAX666': json.loads(self.get('http://ipinfo.io/json').text)['ip']}
        for node in self.lxmlize(url, cookies=cookies).xpath('//ul[@id="candidates"]/li'):
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

            link = node.xpath('.//a[substring(@href, string-length(@href)-11)=".liberal.ca/"]/@href')
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
        for node in self.lxmlize(url).xpath('//div[contains(@class,"tshowcase-inner-box")]'):
            name = node.xpath('.//div[@class="tshowcase-box-title"]//text()')
            if name:
                district = node.xpath('.//div[@class="tshowcase-single-position"]//text()')
                if district:
                    district = district[0].replace('- ', '—').replace(' – ', '—').replace('–', '—').replace('\u200f', '').strip()  # hyphen, n-dash, n-dash, RTL mark
                else:
                    district = 'TBD'  # will be skipped

                if district in DIVISIONS_MAP:
                    district = DIVISIONS_MAP[district]
                elif district in DIVISIONS_M_DASH:
                    district = district.replace('-', '—')  # hyphen, m-dash

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
                            p.add_contact('email', email[0].replace(url, ''))

                    self.add_links(p, node)

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

        url = 'http://www.ndp.ca/candidates'
        birth_date = 1900
        for node in self.lxmlize(url, encoding='utf-8').xpath('//div[@class="candidate-holder"]'):
            image = node.xpath('.//div/@data-img')[0]

            name = node.xpath('.//div[@class="candidate-name"]//text()')[0]
            district = re.search(r'\d{5}', image).group(0)  # node.xpath('.//span[@class="candidate-riding-name"]/text()')[0]

            p = Person(primary_org='lower', name=name, district=district, role='candidate', party='NDP')
            p.image = image

            # There are two Erin Weir.
            if name == 'Erin Weir':
                p.birth_date = str(birth_date)
                birth_date += 1

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
                p.add_link(facebook[0])

            email = None
            link = node.xpath('.//a[@class="candidate-website"]/@href')
            if link:
                p.add_link(link[0])

                node = self.lxmlize(link[0]).xpath('//div[@class="contact-phone"]')
                if node:
                    email = self.get_email(node[0], error=False)
                    if email:
                        p.add_contact('email', email)

                    voice = self.get_phone(node[0], error=False)
                    if voice:
                        p.add_contact('voice', voice, 'office')

            if not email and emails.get(int(district)):
                p.add_contact('email', emails[int(district)])

            if name in self.incumbents:
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
                elif 'facebook.com' in link and '?' in link:
                    link = re.sub(r'\?f?ref=.+', '', link)
                elif 'twitter.com' in link:
                    if '@' in link:
                        link = link.replace('@', '')
                    if link.startswith('http://'):
                        link = link.replace('http://twitter.com/', 'https://twitter.com/')
                p.add_link(link)

DIVISIONS_MAP = {
    # Typo.
    "Courtney-Alberni": "Courtenay—Alberni",
    "Grand Prairie MacKenzie": "Grande Prairie—Mackenzie",
    "Honor---Mercier": "Honoré-Mercier",
    "North Burnaby—Seymour": "Burnaby North—Seymour",
    "North Okangan-Shuswap": "North Okanagan—Shuswap",
    "Richmond": "Richmond Centre",
    "Rosement―La Petite-Patrie": "Rosemont—La Petite-Patrie",
    "Ville-Marie―Le Sud-Ouest―île-des-Sœurs": "Ville-Marie—Le Sud-Ouest—Île-des-Soeurs", # hyphens
    'Ville-Marie—Le Sud-Ouest—Île-des-Sœurs': "Ville-Marie—Le Sud-Ouest—Île-des-Soeurs", # m-dashes
    "Ville-Marie―Le Sud-Ouest―Îles-des-Soeurs": "Ville-Marie—Le Sud-Ouest—Île-des-Soeurs",
    # Hyphens.
    "Barrie-Springwater-Oro-Medonte": "Barrie—Springwater—Oro-Medonte",  # last hyphen
    "Chatham-Kent-Leamington": "Chatham-Kent—Leamington",  # first hyphen
    "Edmonton-Griesbach": "Edmonton Griesbach",
    "Edmonton-Manning": "Edmonton Manning",
    "Vancouver-Granville": "Vancouver Granville",
    # Spaces.
    "Brossard-Saint Lambert": "Brossard—Saint-Lambert",
    "Edmonton Wetaskiwin": "Edmonton—Wetaskiwin",
    "London Fanshawe": "London—Fanshawe",
    "Perth Wellington": "Perth—Wellington",
    "Rivière des Mille Îles": "Rivière-des-Mille-Îles",
    # Capitalization.
    "Montmagny―L’Islet―Kamouraska―Rivière-du-loup": "Montmagny—L'Islet—Kamouraska—Rivière-du-Loup",
}

# @note Can cut down the line count of this file by doing this dynamically.
DIVISIONS_M_DASH = (  # none of the districts use m-dashes
    "Abitibi-Baie-James-Nunavik-Eeyou",
    "Abitibi-Témiscamingue",
    "Acadie-Bathurst",
    "Algoma-Manitoulin-Kapuskasing",
    "Argenteuil-La Petite-Nation",
    "Aurora-Oak Ridges-Richmond Hill",
    "Avignon-La Mitis-Matane-Matapédia",
    "Banff-Airdrie",
    "Barrie-Innisfil",
    "Barrie-Springwater-Oro-Medonte",
    "Battle River-Crowfoot",
    "Battlefords-Lloydminster",
    "Beaches-East York",
    "Beauport-Côte-de-Beaupré-Île d’Orléans-Charlevoix",
    "Beauport-Limoilou",
    "Bellechasse-Les Etchemins-Lévis",
    "Beloeil-Chambly",
    "Berthier-Maskinongé",
    "Bonavista-Burin-Trinity",
    "Brandon-Souris",
    "Brantford-Brant",
    "Brome-Missisquoi",
    "Brossard-Saint-Lambert",
    "Bruce-Grey-Owen Sound",
    "Burnaby North-Seymour",
    "Bécancour-Nicolet-Saurel",
    "Cape Breton-Canso",
    "Cariboo-Prince George",
    "Carlton Trail-Eagle Creek",
    "Central Okanagan-Similkameen-Nicola",
    "Charlesbourg-Haute-Saint-Charles",
    "Charleswood-St. James-Assiniboia-Headingley",
    "Chatham-Kent-Leamington",
    "Chicoutimi-Le Fjord",
    "Chilliwack-Hope",
    "Churchill-Keewatinook Aski",
    "Châteauguay-Lacolle",
    "Cloverdale-Langley City",
    "Coast of Bays-Central-Notre Dame",
    "Compton-Stanstead",
    "Coquitlam-Port Coquitlam",
    "Courtenay-Alberni",
    "Cowichan-Malahat-Langford",
    "Cumberland-Colchester",
    "Cypress Hills-Grasslands",
    "Dartmouth-Cole Harbour",
    "Dauphin-Swan River-Neepawa",
    "Desnethé-Missinippi-Churchill River",
    "Dorval-Lachine-LaSalle",
    "Dufferin-Caledon",
    "Edmonton-Wetaskiwin",
    "Eglinton-Lawrence",
    "Elgin-Middlesex-London",
    "Elmwood-Transcona",
    "Esquimalt-Saanich-Sooke",
    "Etobicoke-Lakeshore",
    "Flamborough-Glanbrook",
    "Fleetwood-Port Kells",
    "Fort McMurray-Cold Lake",
    "Gaspésie-Les Îles-de-la-Madeleine",
    "Glengarry-Prescott-Russell",
    "Grande Prairie-Mackenzie",
    "Haldimand-Norfolk",
    "Haliburton-Kawartha Lakes-Brock",
    "Hamilton East-Stoney Creek",
    "Hamilton West-Ancaster-Dundas",
    "Hastings-Lennox and Addington",
    "Hull-Aylmer",
    "Humber River-Black Creek",
    "Huron-Bruce",
    "Kamloops-Thompson-Cariboo",
    "Kanata-Carleton",
    "Kelowna-Lake Country",
    "Kildonan-St. Paul",
    "Kings-Hants",
    "King-Vaughan",
    "Kitchener South-Hespeler",
    "Kitchener-Conestoga",
    "Kootenay-Columbia",
    "Lambton-Kent-Middlesex",
    "Lanark-Frontenac-Kingston",
    "Langley-Aldergrove",
    "LaSalle-Émard-Verdun",
    "Laurentides-Labelle",
    "Laurier-Sainte-Marie",
    "Laval-Les Îles",
    "Leeds-Grenville-Thousand Islands and Rideau Lakes",
    "London-Fanshawe",
    "Longueuil-Charles-LeMoyne",
    "Longueuil-Saint-Hubert",
    "Lévis-Lotbinière",
    "Madawaska-Restigouche",
    "Markham-Stouffville",
    "Markham-Thornhill",
    "Markham-Unionville",
    "Medicine Hat-Cardston-Warner",
    "Miramichi-Grand Lake",
    "Mission-Matsqui-Fraser Canyon",
    "Mississauga East-Cooksville",
    "Mississauga-Erin Mills",
    "Mississauga-Lakeshore",
    "Mississauga-Malton",
    "Mississauga-Streetsville",
    "Moncton-Riverview-Dieppe",
    "Montmagny-L'Islet-Kamouraska-Rivière-du-Loup",
    "Moose Jaw-Lake Centre-Lanigan",
    "Mégantic-L'Érable",
    "Nanaimo-Ladysmith",
    "New Westminster-Burnaby",
    "Newmarket-Aurora",
    "Nipissing-Timiskaming",
    "North Island-Powell River",
    "North Okanagan-Shuswap",
    "Northumberland-Peterborough South",
    "Notre-Dame-de-Grâce-Westmount",
    "Oakville North-Burlington",
    "Ottawa West-Nepean",
    "Ottawa-Vanier",
    "Parkdale-High Park",
    "Parry Sound-Muskoka",
    "Peace River-Westlock",
    "Perth-Wellington",
    "Peterborough-Kawartha",
    "Pickering-Uxbridge",
    "Pierre-Boucher-Les Patriotes-Verchères",
    "Pierrefonds-Dollard",
    "Pitt Meadows-Maple Ridge",
    "Port Moody-Coquitlam",
    "Portage-Lisgar",
    "Portneuf-Jacques-Cartier",
    "Prince George-Peace River-Northern Rockies",
    "Red Deer-Lacombe",
    "Red Deer-Mountain View",
    "Regina-Lewvan",
    "Regina-Qu'Appelle",
    "Regina-Wascana",
    "Renfrew-Nipissing-Pembroke",
    "Richmond-Arthabaska",
    "Rimouski-Neigette-Témiscouata-Les Basques",
    "Rosemont-La Petite-Patrie",
    "Saanich-Gulf Islands",
    "Sackville-Preston-Chezzetcook",
    "Saint Boniface-Saint Vital",
    "Saint John-Rothesay",
    "Saint-Hyacinthe-Bagot",
    "Saint-Léonard-Saint-Michel",
    "Saint-Maurice-Champlain",
    "Salaberry-Suroît",
    "Sarnia-Lambton",
    "Saskatoon-Grasswood",
    "Saskatoon-University",
    "Scarborough-Agincourt",
    "Scarborough-Guildwood",
    "Scarborough-Rouge Park",
    "Selkirk-Interlake-Eastman",
    "Sherwood Park-Fort Saskatchewan",
    "Simcoe-Grey",
    "Skeena-Bulkley Valley",
    "Souris-Moose Mountain",
    "South Okanagan-West Kootenay",
    "South Shore-St. Margarets",
    "South Surrey-White Rock",
    "Spadina-Fort York",
    "St. Albert-Edmonton",
    "St. John's South-Mount Pearl",
    "Steveston-Richmond East",
    "Stormont-Dundas-South Glengarry",
    "Sturgeon River-Parkland",
    "Surrey-Newton",
    "Sydney-Victoria",
    "Thunder Bay-Rainy River",
    "Thunder Bay-Superior North",
    "Timmins-James Bay",
    "Tobique-Mactaquac",
    "Toronto-Danforth",
    "Toronto-St. Paul's",
    "University-Rosedale",
    "Vaudreuil-Soulanges",
    "Vaughan-Woodbridge",
    "Ville-Marie-Le Sud-Ouest-Île-des-Soeurs",
    "Wellington-Halton Hills",
    "West Vancouver-Sunshine Coast-Sea to Sky Country",
    "Windsor-Tecumseh",
    "York South-Weston",
    "Yorkton-Melville",
    "York-Simcoe",
)
