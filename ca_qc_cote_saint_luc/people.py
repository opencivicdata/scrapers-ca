# coding: utf-8
from utils import CanadianScraper, CanadianPerson as Person, CUSTOM_USER_AGENT

import re
from urllib.parse import urljoin

COUNCIL_PAGE = 'https://cotesaintluc.org/city-government/council/#councilmembers'

class CoteSaintLucPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE, user_agent=CUSTOM_USER_AGENT)
        councillors = page.xpath('//section[contains(@class,"avia-team-member")]')[:-1]

        for councillor in councillors:
           
            name = councillor.xpath('.//h3/text()')[0] 
            assert len(councillors), 'No councillors found'
            roles = councillor.xpath('.//div[contains(@class,"team-member-job-title")]/text()')
                
            for i in roles:
                sep = ','
                role = i.split(sep, 1)[0]
                district=i.split(sep,1)[-1]

            image= councillor.xpath('.//img/@data-src')[0]
            p = Person(primary_org='legislature', name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)
            p.add_contact('email', self.get_email(councillor))   
            p.add_contact('voice', self.get_phone(councillor, area_codes=[514]), 'legislature')
            p.image = image

            if councillor.xpath('.//p[contains(.,"Twitter")]/a/text()'):
                p.add_link(councillor.xpath('.//p[contains(.,"Twitter")]/a/text()')[0])         
            
            if councillor.xpath('.//p[contains(.,"Web")]/a/@href'):
                p.add_link(councillor.xpath('.//p[contains(.,"Web")]/a/@href')[0])   


            if councillor.xpath('.//p[contains(.,"Blog")]/a/@href'):
                p.add_link(councillor.xpath('.//p[contains(.,"Blog")]/a/@href')[0])   

            yield p

















