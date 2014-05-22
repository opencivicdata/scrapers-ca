# coding: utf8
from pupa.scrape import Scraper

from utils import lxmlize, CanadianLegislator as Legislator

import re
import urllib
import HTMLParser

COUNCIL_PAGE = 'http://www.ville.levis.qc.ca/Fr/Conseil/'


class LevisPersonScraper(Scraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)

    people_links = page.xpath('//h3')
    for person in people_links:
      name, position = person.text.split(' - ')
      if ',' in position:
        role, district = position.title().split(', ')
      else:
        role = 'Maire'
        district = u'Lévis'

      info_div = person.xpath('./following-sibling::div[1]')[0]
      photo_url = info_div[0].attrib['src']
      role = 'Conseiller'
      email = info_div.xpath('string(.//a/@href)')[len('mailto:'):]

      p = Legislator(name=name, post_id=district, role=role)
      p.add_source(COUNCIL_PAGE)
      p.image = photo_url
      p.add_contact('email', email, None)
      yield p
