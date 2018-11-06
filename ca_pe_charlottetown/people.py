from utils import CanadianScraper, CanadianPerson as Person

import re

COUNCIL_PAGE = 'https://www.charlottetown.ca/mayor___council/city_council/meet_my_councillor'


class CharlottetownPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        nodes = page.xpath('//div[@id="ctl00_ContentPlaceHolder1_ctl14_divContent"]/*')
        groups = [[]]
        for node in nodes:
            if node.tag == 'hr':
                groups.append([])
            else:
                groups[-1].append(node)

        assert len(groups), 'No councillors found'
        for group in groups:
            para = group[0]
            match = re.search(r'(Mayor|Councillor) (.+?)(?: - (Ward \d+)(?: \([^)]+\))?)?$', para.xpath('.//strong[1]/text()')[0])
            image = para.xpath('.//@src')[0]

            role = match.group(1)
            name = match.group(2)
            if role == 'Mayor':
                district = 'Charlottetown'
            else:
                district = match.group(3)

            p = Person(primary_org='legislature', name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)

            p.image = image
            email = self.get_email(para, error=False)
            if email:
                p.add_contact('email', email)

            for text in para.xpath('.//strong[contains(., "Phone")]/following-sibling::text()'):
                if re.search(r'\d', text):
                    match = re.search(r'(.+) \((.+)\)', text)
                    if match.group(2) == 'Fax':
                        contact_type = 'fax'
                    else:
                        contact_type = 'voice'
                    p.add_contact(contact_type, match.group(1), match.group(2))

            yield p
