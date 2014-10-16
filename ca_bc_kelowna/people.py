# coding: utf-8
from __future__ import unicode_literals
from pupa.scrape import Scraper

import re

from utils import lxmlize, CanadianPerson as Person

COUNCIL_PAGE = 'http://www.kelowna.ca/CM/Page159.aspx'


class KelownaPersonScraper(Scraper):

  def scrape(self):
    page = lxmlize(COUNCIL_PAGE)
    links = page.xpath('//td[@width=720]//a[contains(text(), "Councillor") or '
                       'contains(text(), "Mayor")]')
    for link in links:
      role, name = link.text_content().replace('\xa0', ' ').split(' ', 1)
      url = link.attrib['href']
      page = lxmlize(url)
      photo_url = page.xpath('string(//li/img/@src)')
      phone = page.xpath('//strong')[-1].text_content()
      email = page.xpath('string(//a[starts-with(@href, "mailto:")])')

      p = Person(name=name, district='Kelowna', role=role, image=photo_url)
      p.add_source(COUNCIL_PAGE)
      p.add_source(url)
      p.add_contact('voice', phone, 'legislature')
      p.add_contact('email', email, None)
      yield p
