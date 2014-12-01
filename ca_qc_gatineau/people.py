from __future__ import unicode_literals
from utils import CanadianScraper, CanadianPerson as Person

import re

COUNCIL_PAGE = 'http://www.gatineau.ca/page.asp?p=la_ville/conseil_municipal'
MAYOR_CONTACT_PAGE = 'http://www.gatineau.ca/portail/default.aspx?p=la_ville/conseil_municipal/maire'


class GatineauPersonScraper(CanadianScraper):

    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        # it's all javascript rendered on the client... wow.
        js = page.xpath('string(//div[@class="inner_container"]/div/script[2])')
        districts = re.findall(r'arrayDistricts\[a.+"(.+)"', js)
        members = re.findall(r'arrayMembres\[a.+"(.+)"', js)
        urls = re.findall(r'arrayLiens\[a.+"(.+)"', js)
        # first item in list is mayor
        p = Person(primary_org='legislature', name=members[0], district='Gatineau', role='Maire')
        p.add_source(COUNCIL_PAGE)
        p.add_source(MAYOR_CONTACT_PAGE)
        email = 'maire@gatineau.ca'  # @todo hardcoded
        p.add_contact('email', email)
        yield p

        for raw_district, member, url in list(zip(districts, members, urls))[1:]:
            profile_url = COUNCIL_PAGE + '/' + url.split('/')[-1]
            profile_page = self.lxmlize(profile_url)
            photo_url = profile_page.xpath('//img/@src')[0]
            district = 'District ' + re.search('\d+', raw_district).group(0)
            email = profile_page.xpath(
                'string(//a[contains(@href, "mailto:")]/@href)')[len('mailto:'):]
            p = Person(primary_org='legislature', name=member, district=district, role='Conseiller')
            p.add_source(COUNCIL_PAGE)
            p.add_source(profile_url)
            p.image = photo_url
            p.add_contact('email', email)
            yield p
