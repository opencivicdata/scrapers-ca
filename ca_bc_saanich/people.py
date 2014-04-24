# coding: utf-8
from __future__ import unicode_literals

from pupa.scrape import Scraper

from utils import lxmlize, CanadianLegislator as Legislator

import re

COUNCIL_PAGE = 'http://www.saanich.ca/living/mayor/council/index.html'


class SaanichPersonScraper(Scraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)
    for link in page.xpath('//div[@class="section"]//a'):
      url = link.attrib['href']
      if url.endswith('address.html'):
        continue
      page = lxmlize(url)
      role, name = page.xpath('string(//div[@id="content"]/h1)').split(' ', 1)
      name = ' '.join(name.split()[:-1])
      photo_url = page.xpath('string(//img[@class="float-right"]/@src)')
      email = page.xpath('string(//a[starts-with(@href, "mailto:")])')

      p = Legislator(name=name, post_id='Saanich', role=role, image=photo_url)
      p.add_source(COUNCIL_PAGE)
      p.add_source(url)
      p.add_contact('email', email, None)
      yield p
