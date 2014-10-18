from __future__ import unicode_literals
from utils import CanadianScraper, CanadianPerson as Person

import re

COUNCIL_PAGE = 'http://www.assembly.pe.ca/index.php3?number=1024584&lang=E'


class PrinceEdwardIslandPersonScraper(CanadianScraper):

    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)
        table = page.cssselect('table')[0]
        rows = table.cssselect('tr')[1:]
        assert len(rows) == 27  # There should be 27 districts

        for row in rows:
            districtnumcell, districtcell, membercell, dummy2 = row.cssselect('td')

            district_name = districtcell.cssselect('a')[0].text_content().strip()
            district = district_name.replace(' - ', '-')
            name = (membercell.cssselect('a')[0].text_content().replace('Hon. ', '')
                    .replace(' (LIB)', '').replace(' (PC)', '').strip())
            url = membercell.cssselect('a')[0].get('href')
            email, phone, photo_url = self.scrape_extended_info(url)
            p = Person(primary_org='legislature', name=name, district=district, role='MLA', image=photo_url)
            p.add_source(COUNCIL_PAGE)
            p.add_source(url)
            p.add_contact('email', email)
            p.add_contact('voice', phone, 'legislature')
            yield p

    def scrape_extended_info(self, url):
        root = self.lxmlize(url)
        main = root.cssselect('#content table')[0]
        photo_url = main.cssselect('img')[0].get('src')
        contact_cell = main.cssselect('td:contains("Contact information")')[0]
        phone = re.search(r'(?:Telephone|Tel|Phone):(.+?)\n', contact_cell.text_content()).group(1)
        email = contact_cell.cssselect('a[href^=mailto]')[0].get('href').replace('mailto:', '')
        return email, phone, photo_url
