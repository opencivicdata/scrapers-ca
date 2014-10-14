# coding: utf-8
from __future__ import unicode_literals
from pupa.scrape import Scraper

import re

from six.moves.urllib.parse import urljoin

from utils import lxmlize, CanadianPerson as Person

COUNCIL_PAGE = 'http://www.kitchener.ca/en/insidecityhall/WhoIsMyCouncillor.asp'
MAYOR_PAGE = 'http://www.kitchener.ca/en/insidecityhall/MayorSLandingPage.asp'


class KitchenerPersonScraper(Scraper):

  def scrape(self):
    page = lxmlize(COUNCIL_PAGE)

    councillor_nodes = page.xpath('//div[@id="printArea"]//li')

    for node in councillor_nodes:
      councillor_url = node.xpath('string(./a/@href)')
      ward = node.xpath('string(./strong)').split('-')[0]
      yield councillor_data(councillor_url, ward)

    yield mayor_data(MAYOR_PAGE)


def councillor_data(url, ward):
  page = lxmlize(url)

  infobox_node = page.xpath('//div[@id="printArea"]')[0]
  name = infobox_node.xpath('string(.//h1[1])')[len('Councillor'):]

  contact_node = infobox_node.xpath('.//p[contains(text(), "Coun.")]')[0]
  email = contact_node.xpath('string(.//text()[contains(., "@")])').split()[-1]

  # TODO: contact details are tricky
  #address = '\n'.join(contact_node.xpath('./text()')[:4])
  #phone = contact_node.xpath('string(./text()[5])').strip('City hall:')

  photo_url_rel = page.xpath('string(//div[@id="sideBar"]//img/@src)')
  photo_url = urljoin(COUNCIL_PAGE, photo_url_rel)

  p = Person(name=name, post_id=ward, role='Councillor')
  p.add_source(COUNCIL_PAGE)
  p.add_source(url)
  if email:
    p.add_contact('email', email, None)
  p.image = photo_url

  return p


def mayor_data(url):
  page = lxmlize(url)

  infobox_node = page.xpath('//div[@id="printArea"]')[0]
  name = infobox_node.xpath('string(.//h1)')[6:]  # strip 'Mayor' prefix

  contact_node = page.xpath('//div[@id="contentIntContact"]')[0]

  # TODO: fruitlessly wasted way too much time below
  address = '\n'.join(contact_node.xpath('./p[2]/text()')[:3])
  phone = contact_node.xpath('string(./p[2]/text()[contains(., "T.")])')[3:]

  photo_url_rel = page.xpath('string(//div[@id="sideBar"]//img/@src)')
  photo_url = urljoin(COUNCIL_PAGE, photo_url_rel)

  p = Person(name=name, post_id='Kitchener', role='Mayor')
  p.add_source(url)
  p.image = photo_url

  return p
