# coding: utf-8
from __future__ import unicode_literals

from pupa.scrape import Scraper

from utils import lxmlize, CanadianLegislator as Legislator

import re

COUNCIL_PAGE = 'http://www.coquitlam.ca/city-hall/mayor-and-council/mayor-and-council.aspx'


class CoquitlamPersonScraper(Scraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)
    for person_link in page.xpath('//a[@class="L4"]'):
        role, name = person_link.text_content().split(' ', 1)
        url = person_link.attrib['href']
        page = lxmlize(url)
        photo_url = page.xpath('string(//img[@class="img-right"]/@src)')
        email = page.xpath('string(//a[starts-with(@href, "mailto:")])')

        p = Legislator(name=name, post_id='Coquitlam', role=role, image=photo_url)
        p.add_source(COUNCIL_PAGE)
        p.add_source(url)
        p.add_contact('email', email, None)
        yield p
