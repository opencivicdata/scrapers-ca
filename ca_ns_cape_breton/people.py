from utils import CanadianScraper, CanadianPerson as Person

import re

COUNCIL_PAGE = 'http://www.cbrm.ns.ca/councillors.html'
MAYOR_PAGE = 'http://www.cbrm.ns.ca/mayor.html'


class CapeBretonPersonScraper(CanadianScraper):

    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        councillors = page.xpath('//table/tbody/tr')[1:]
        assert len(councillors), 'No councillors found'
        for councillor in councillors:
            name = councillor.xpath('./td[2]//text()')[0]
            if 'District ' in name:  # Vacant
                continue
            district = 'District {}'.format(councillor.xpath('.//strong')[0].text_content())

            address = councillor.xpath('.//td')[2].text_content().replace("\r\n", ', ')
            contact_nodes = councillor.xpath('.//td[4]/text()')
            if ':' not in contact_nodes[0]:
                contact_nodes = councillor.xpath('.//td[4]/p/text()')

            phone = contact_nodes[0].split(':')[1].replace("(", '').replace(") ", '-')
            if 'or' in phone:  # phone and cell
                phone = phone.split('or')[0]

            # email protected by js
            clean_name = name.replace('“', '"').replace('”', '"')
            p = Person(primary_org='legislature', name=clean_name, district=district, role='Councillor')
            p.add_source(COUNCIL_PAGE)
            p.add_contact('address', address, 'legislature')
            p.add_contact('voice', phone, 'legislature')

            if 'F' in contact_nodes[1]:
                fax = contact_nodes[1].split(':')[1].replace("(", '').replace(") ", '-')
                p.add_contact('fax', fax, 'legislature')

            councillor_url = councillor.xpath('.//a/@href')[0]
            p.add_source(councillor_url)
            page = self.lxmlize(councillor_url)
            image = page.xpath('//img[contains(@title, "{0}")]/@src'.format(name))
            if image:
                p.image = image[0]
            yield p

        mayorpage = self.lxmlize(MAYOR_PAGE)

        mayor_name_nodes = mayorpage.xpath('//p/*[contains(text(), "Mayor")]//text()')
        for node in mayor_name_nodes:
            result = re.search('Mayor ([A-Z].+ [A-Z].+[^:])', node)
            if result is not None:
                name = result.group(1)
                break

        photo_url = mayorpage.xpath('//span/img/@src')[0]
        contact_nodes = mayorpage.xpath('//aside//h3[contains(text(), "Contact")]/following-sibling::div[1]')[0]
        address = contact_nodes.xpath('.//p[1]/text()')[0]
        phone = contact_nodes.xpath('.//p[2]/text()')[0].split(': ')[1]
        fax = contact_nodes.xpath('.//p[2]/text()')[1].split(': ')[1]
        email = self.get_email(contact_nodes.xpath('.//p[3]')[0])

        p = Person(primary_org='legislature', name=name, district='Cape Breton', role='Mayor')
        p.add_source(MAYOR_PAGE)
        p.add_contact('address', address, 'legislature')
        p.add_contact('voice', phone, 'legislature')
        p.add_contact('email', email)
        p.image = photo_url
        yield p
