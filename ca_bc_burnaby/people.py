# coding: utf-8
from __future__ import unicode_literals
from utils import CanadianScraper, CanadianPerson as Person

COUNCIL_PAGE = 'http://www.burnaby.ca/Our-City-Hall/Mayor---Council/Council-Profiles.html'


class BurnabyPersonScraper(CanadianScraper):

    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        for person_url in page.xpath('//h4/a/@href'):
            page = self.lxmlize(person_url)

            role, name = page.xpath('string(//title)').split(' ', 1)
            photo_url = page.xpath('string(//div[@id="content"]//img[@style]/@src)')
            email = page.xpath('string(//a[contains(@href, "mailto:")])')
            phone = page.xpath('string(//li[contains(text(), "Phone:")])')

            p = Person(primary_org='legislature', name=name, district='Burnaby', role=role, image=photo_url)
            p.add_source(COUNCIL_PAGE)
            p.add_source(person_url)
            p.add_contact('email', email)
            if phone:
                p.add_contact('voice', phone, 'legislature')
            yield p
