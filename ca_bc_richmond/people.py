# coding: utf-8
from __future__ import unicode_literals
from pupa.scrape import Scraper

import re

from utils import lxmlize, CanadianPerson as Person

COUNCIL_PAGE = 'http://www.richmond.ca/cityhall/council.htm'
CONTACT_URL = 'http://www.richmond.ca/contact/departments/council.htm'


class RichmondPersonScraper(Scraper):

  def scrape(self):
    contact_page = lxmlize(CONTACT_URL)
    email = contact_page.xpath('string(//a[starts-with(@href, "mailto:")])')
    page = lxmlize(COUNCIL_PAGE)
    for url in page.xpath('//a/@href[contains(., "members/")]'):
      page = lxmlize(url)
      role, name = page.xpath('string(//h1)').split(' ', 1)
      # image element is inserted by a script somewhere
      #photo_url = page.xpath('string(//span[@class="imageShadow"]/img/@src)')

      p = Person(name=name, district='Richmond', role=role)
      p.add_source(COUNCIL_PAGE)
      p.add_source(CONTACT_URL)
      p.add_source(url)
      p.add_contact('email', email, None)
      yield p
