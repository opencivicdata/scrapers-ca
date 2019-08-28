from utils import CanadianScraper, CanadianPerson as Person

import re

COUNCIL_PAGE = 'https://www.surrey.ca/city-government/2999.aspx'

class SurreyPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)
        members = page.xpath("//a[@class='gtm-grid']")

        assert len(members), 'No members found'
        seat_number = 1
        for member in members:
            if not member.text_content().strip():
                continue

            name = member.text_content().strip()
            district = 'Surrey (seat {})'.format(seat_number)
            seat_number += 1
            role = 'Councillor'

            url = member.attrib['href']
            ext_infos = self.scrape_extended_info(url)
            p = Person(primary_org='legislature', name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)
            p.add_source(url)

            if ext_infos:  # member pages might return errors
                email, phone, photo_url = ext_infos
                if photo_url:
                    p.image = photo_url
                if email:
                    p.add_contact('email', email)
                if phone:
                    p.add_contact('voice', phone, 'legislature')
            yield p

    def scrape_extended_info(self, url):
        phone = None
        email = None
        root = self.lxmlize(url)
        main = root.xpath("//div[@class='inner-wrapper']")[0]
        photo_url = main.xpath('.//img/@src')
        paras = main.xpath('.//p')
        for para in paras:
            pattern = re.compile('(?:Office: )(.+?)\n(Email: )(.+)')
            matches = re.search(pattern, para.text_content())
            if (matches):
                phone = matches[1]
                email = matches[3]
        return email, phone, photo_url[0]
