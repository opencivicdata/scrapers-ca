# coding: utf-8
from __future__ import unicode_literals
from pupa.scrape import Scraper

import re

from utils import lxmlize, CanadianPerson as Person

COUNCIL_PAGE = 'http://www.ville.levis.qc.ca/Fr/Conseil/'


class LevisPersonScraper(Scraper):

  def scrape(self):
    page = lxmlize(COUNCIL_PAGE)

    people_links = page.xpath('//h3')
    for person in people_links:
      name, position = person.text.split(' - ')
      if ',' in position:
        role, district = position.title().split(', ')
      else:
        role = 'Maire'
        district = 'Lévis'

      info_div = person.xpath('./following-sibling::div[1]')[0]
      photo_url = info_div[0].attrib['src']
      role = 'Conseiller'
      email = info_div.xpath('string(.//a/@href)')[len('mailto:'):]

      p = Person(name=name, district=district, role=role)
      p.add_source(COUNCIL_PAGE)
      p.image = photo_url
      p.add_contact('email', email, None)
      yield p
