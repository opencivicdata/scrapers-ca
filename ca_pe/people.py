from utils import CanadianScraper, CanadianPerson as Person

import re

COUNCIL_PAGE = 'http://www.assembly.pe.ca/current-members'


class PrinceEdwardIslandPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)
        members = page.xpath('//table[1]//tr')

        assert len(members), 'No members found'
        for member in members:
            name = member.xpath('./td[2]//a[1]//text()')[0]

            district_name = member.xpath('./td[2]//a[contains(.//text(), "MLA")]//text()')[0].split(':')[1].replace('St ', 'St. ').split('-')
            district = district_name[0].strip() + '-' + district_name[1].strip()
            url = member.xpath('./td[2]//a[1]/@href')[0]
            ext_infos = self.scrape_extended_info(url)
            p = Person(primary_org='legislature', name=name, district=district, role='MLA')
            p.add_source(COUNCIL_PAGE)
            p.add_source(url)

            if ext_infos:  # member pages might return errors
                email, phone, photo_url = ext_infos
                p.image = photo_url
                if email:
                    p.add_contact('email', email)
                if phone:
                    p.add_contact('voice', phone, 'legislature')
            yield p

    def scrape_extended_info(self, url):
        root = self.lxmlize(url)
        if not root.xpath('//div[contains(@class, "colmask")][contains(@class, "rightmenu")]'):  # Speaker page
            main = root.xpath('//div[@id="content"]//table')[0]
            photo_url = main.xpath('.//img')[0].get('src')
            contact_cell = main.xpath('.//td[contains(., "nformation")]')[0]
            phone = None
            phone_s = re.search(r'(?:Telephone|Tel|Phone):(.+?)\n', contact_cell.text_content())
            if phone_s:
                phone = phone_s.group(1)
            email = self.get_email(contact_cell, error=False)
            return email, phone, photo_url
