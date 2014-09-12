# coding: utf-8
from pupa.scrape import Scraper

from utils import lxmlize, CanadianLegislator as Legislator

import re

COUNCIL_PAGE = 'http://www.stjohns.ca/city-hall/about-city-hall/council'


class StJohnsPersonScraper(Scraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)
    nodes = page.xpath('//div[@class="view-content"]/div')
    for node in nodes:
      fields = node.xpath('./div')
      role = fields[0].xpath('string(./div)')
      name = fields[2].xpath('string(.//a)').title().split(role)[-1]
      if 'Ward' in role:
        post_id = role
        role = 'Councillor'
      else:
        if 'At Large' in role:
          role = 'Councillor'
        post_id = "St. John's"
      phone = fields[3].xpath('string(./div)')
      email = fields[5].xpath('string(.//a)')
      photo_url = node.xpath('string(.//img/@src)')

      p = Legislator(name=name, post_id=post_id, role=role)
      p.add_source(COUNCIL_PAGE)
      p.add_contact('voice', phone, 'legislature')
      p.add_contact('email', email, None)
      p.image = photo_url
      yield p
