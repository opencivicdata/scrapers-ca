# coding: utf-8
from __future__ import unicode_literals
from pupa.scrape import Scraper

import re

from six.moves.urllib.parse import urljoin, unquote

from utils import lxmlize, CanadianPerson as Person

COUNCIL_PAGE = 'http://www.victoria.ca/EN/main/city/mayor-council-committees/councillors.html'


class VictoriaPersonScraper(Scraper):

  def scrape(self):
    page = lxmlize(COUNCIL_PAGE)
    nodes = page.xpath('//div[@id="content"]/ul/li')
    for node in nodes:
      url = urljoin(COUNCIL_PAGE, node.xpath('string(./a/@href)'))
      name = node.xpath('string(./a)')
      yield councillor_data(url, name, 'Councillor')

    mayor_node = page.xpath('(//div[@id="section-navigation-middle"]/ul/li/'
                            'ul/li/a)[1]')[0]
    mayor_url = urljoin(COUNCIL_PAGE, mayor_node.xpath('string(./@href)'))
    mayor_name = mayor_node.xpath('string(.)')
    yield mayor_data(mayor_url, mayor_name, 'Mayor')


def councillor_data(url, name, role):
  page = lxmlize(url)
  email = page.xpath('string(//a[contains(@href, "mailto")])')
  phone_str = page.xpath('string(//div[@id="content"]//strong[1]/'
                         'following-sibling::text()[contains(., "Phone")])')
  phone = phone_str.split(':')[1]
  photo_url = urljoin(url,
                      page.xpath('string(//div[@id="content"]//img[1]/@src)'))

  # TODO: should district be "Nieghborhood Liaison"?
  m = Person(name=name, district='Victoria', role=role)
  m.add_source(COUNCIL_PAGE)
  m.add_source(url)
  m.add_contact('email', email, None)
  m.add_contact('voice', phone, 'legislature')
  m.image = photo_url
  return m


def mayor_data(url, name, role):
  page = lxmlize(url)
  email = unquote((page.xpath('string(//a[contains(@href, "mailto")]/@href)')).
                  split(':')[1])
  phone_str = page.xpath('string(//div[@id="content"]//strong[1]/'
                         'following-sibling::text()[contains(., "phone")])')
  phone = phone_str.split(':')[1]
  photo_url = urljoin(url,
                      page.xpath('string(//div[@id="content"]//img[1]/@src)'))

  # TODO: should district be "Nieghborhood Liaison"?
  m = Person(name=name, district='Victoria', role=role)
  m.add_source(COUNCIL_PAGE)
  m.add_source(url)
  m.add_contact('email', email, None)
  m.add_contact('voice', phone, 'legislature')
  m.image = photo_url
  return m
