from utils import CanadianScraper, CanadianPerson as Person, CONTACT_DETAIL_TYPE_MAP

import re

COUNCIL_PAGE = 'https://www.ajax.ca/en/inside-townhall/council-members.aspx'


class AjaxPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        councillors = page.xpath('//table[@class="councilTable"]')
        for councillor in councillors:
            image = councillor.xpath('.//@src')[0]
            councillor_name = councillor.xpath('.//tr/td[1]/p[1]/img/@alt')
            assert len(councillors), 'No councillors found'
       
            for i in councillor_name:
                sep = '-'
                name = i.split(sep, 1)[0]

            if name == councillor_name[0]:
                district = 'Ajax'
                role = 'Mayor'

            else:
                role=i.split(sep, 1)[-1]
        
            cell = councillor.xpath('.//p[contains(.,"Cel")]/text()')[0]
            tel= councillor.xpath('.//p[contains(.,"Cel")]/text()')[1]
            phone=cell.replace('\xa0', ' ')
           

            p = Person(primary_org='legislature', name=name, district='district', role='role')
            p.add_source(COUNCIL_PAGE)
            p.image=image

            if phone:
                p.add_contact('cell', phone, 'legislature')
            if tel:
                p.add_contact('voice', tel, 'legislature')

            p.add_contact('email', self.get_email(councillor))                

            yield p
