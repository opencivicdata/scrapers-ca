from __future__ import unicode_literals
from utils import CanadianScraper, CanadianPerson as Person

import json
import re

import requests
import scrapelib

DIVISIONS_MAP = {
    # Typo.
    "North Okangan-Shuswap": "North Okanagan—Shuswap",
    # Hyphens.
    "Barrie-Springwater-Oro-Medonte": "Barrie—Springwater—Oro-Medonte",  # last hyphen
    "Chatham-Kent-Leamington": "Chatham-Kent—Leamington",  # first hyphen
    "Vancouver-Granville": "Vancouver Granville",
    # Spaces.
    "Brossard-Saint Lambert": "Brossard—Saint-Lambert",
    "Perth Wellington": "Perth—Wellington",
    "Rivière des Mille Îles": "Rivière-des-Mille-Îles",
}

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

class CanadaCandidatesPersonScraper(CanadianScraper):

    def scrape(self):
        representatives = json.loads(self.get('http://represent.opennorth.ca/representatives/house-of-commons/?limit=0').text)['objects']
        incumbents = [representative['name'] for representative in representatives]

        # http://www.blocquebecois.org/equipe-2015/circonscriptions/candidats/
        # http://www.forcesetdemocratie.org/l-equipe/candidats.html
        # https://www.libertarian.ca/candidates/

        url = 'http://www.conservative.ca/wp-content/themes/conservative/scripts/candidates.json'
        for nodes in json.loads(self.get(url).text).values():
            for node in nodes:
                if node['district'] == 'Whitby-Oshawa':  # @todo not sure what it became
                    continue
                elif node['district'] == 'Vancouver-Granville':
                    node['district'] = 'Vancouver Granville'

                name = node['candidate']
                district = node['district'].replace(' – ', '—').replace(' ', ' ').strip()  # n-dash, m-dash, non-breaking space

                if district in DIVISIONS_MAP:
                    district = DIVISIONS_MAP[district]
                elif district in DIVISIONS_M_DASH:
                    district = district.replace('-', '—')  # hyphen, m-dash

                p = Person(primary_org='lower', name=name, district=district, role='candidate', party='Conservative')
                p.image = 'http://www.conservative.ca/media/candidates/{}'.format(node['image'])

                if name in incumbents:
                    p.extras['incumbent'] = True

                p.add_source(url)
                yield p

        url = 'http://www.greenparty.ca/en/candidates'
        for node in self.lxmlize(url).xpath('//div[contains(@class,"candidate-card")]'):
            name = node.xpath('.//div[@class="candidate-name"]//text()')[0].replace('Mark & Jan', 'Mark')
            district = node.xpath('.//@data-target')[0][5:]  # node.xpath('.//div[@class="riding-name"]//text()')[0]

            p = Person(primary_org='lower', name=name, district=district, role='candidate', party='Green Party')
            p.image = node.xpath('.//img[@typeof="foaf:Image"]/@src')[0]  # print quality also available

            p.add_contact('email', self.get_email(node))

            link = node.xpath('.//div[@class="margin-bottom-gutter"]/a[contains(@href,"http")]/@href')
            if link:
                p.add_link(link[0])
            self.add_links(p, node)

            if name in incumbents:
                p.extras['incumbent'] = True

            p.add_source(url)
            yield p

        url = 'https://www.liberal.ca/candidates/'
        for node in self.lxmlize(url).xpath('//ul[@id="candidates"]/li'):
            name = node.xpath('./h2/text()')[0]
            district = node.xpath('./@data-riding-riding_id')[0]  # node.xpath('./@data-riding-name')[0]

            # @note Remove once corrected.
            if name == 'Nicola Di lorio':
                name = 'Nicola Di Iorio'

            p = Person(primary_org='lower', name=name, district=district, role='candidate', party='Liberal')
            p.image = node.xpath('./@data-photo-url')[0][4:-1]

            if node.xpath('./@class[contains(.,"candidate-female")]'):
                p.gender = 'female'
            elif node.xpath('./@class[contains(.,"candidate-male")]'):
                p.gender = 'male'

            link = node.xpath('.//a[substring(@href, string-length(@href)-11)=".liberal.ca/"]/@href')
            self.add_links(p, node)

            if link:
                try:
                    # http://susanwatt.liberal.ca/ redirects to http://www.liberal.ca/
                    sidebar = self.lxmlize(link[0]).xpath('//div[@id="sidebar"]')
                    if sidebar:
                        email = self.get_email(sidebar[0], error=False)
                        if email:
                            p.add_contact('email', email)
                        voice = self.get_phone(sidebar[0], error=False)
                        if voice:
                            p.add_contact('voice', voice, 'legislature')

                        p.add_link(link[0])
                except (requests.exceptions.ConnectionError, scrapelib.HTTPError):
                    pass

            if name in incumbents:
                p.extras['incumbent'] = True

            p.add_source(url)
            yield p

        url = 'http://www.ndp.ca/candidates'
        for node in self.lxmlize(url, encoding='utf-8').xpath('//div[@class="candidate-holder"]'):
            image = node.xpath('.//div/@data-img')[0]

            name = node.xpath('.//div[@class="candidate-name"]//text()')[0]
            district = re.search(r'\d{5}', image).group(0)  # node.xpath('.//span[@class="candidate-riding-name"]/text()')[0]

            p = Person(primary_org='lower', name=name, district=district, role='candidate', party='NDP')
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
                if 'www.ndp.ca' in facebook[0]:
                    facebook[0] = facebook[0].replace('www.ndp.ca', 'www.facebook.com')
                p.add_link(facebook[0])
            link = node.xpath('.//a[@class="candidate-website"]/@href')
            if link:
                p.add_link(link[0])

            if name in incumbents:
                p.extras['incumbent'] = True

            p.add_source(url)
            yield p

    def add_links(self, p, node):
        for substring in ('facebook.com', 'fb.com', 'instagram.com', 'linkedin.com', 'twitter.com', 'youtube.com'):
            link = self.get_link(node, substring, error=False)
            if link:
                if link[:3] == 'ttp':
                    link = 'h' + link
                p.add_link(link)
