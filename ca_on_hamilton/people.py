# coding: utf-8
from __future__ import unicode_literals
from pupa.scrape import Scraper

import re

from utils import lxmlize, CanadianPerson as Person

COUNCIL_PAGE = 'http://www.hamilton.ca/YourElectedOfficials/WardCouncillors/'


class HamiltonPersonScraper(Scraper):

  def scrape(self):
    page = lxmlize(COUNCIL_PAGE)
    council_node = page.xpath('//span[@id="RadEditorPlaceHolderControl0"]')[0]
    councillor_urls = council_node.xpath('./table[2]//p/a[not(img)]/@href')

    for councillor_url in councillor_urls:
      yield councillor_data(councillor_url)

    yield mayor_data(council_node.xpath('./table[1]/tbody/tr')[0])


def councillor_data(url):
  page = lxmlize(url)

  name, district = page.xpath('string(//span[@id="_hpcPageTitle"])').split('-')

  info_node = page.xpath('//span[@id="RadEditorPlaceHolderControl0"]')[0]
  # strip the word 'Phone:' from the beginning of the number
  phone = info_node.xpath('string(.//b[1])')[7:]
  email = info_node.xpath('string(.//a)')
  photo_url = info_node.xpath('string(.//img/@src)')

  p = Person(name=name, district=district, role='Councillor')
  p.add_source(COUNCIL_PAGE)
  p.add_source(url)
  p.add_contact('email', email, None)

  if phone:
    p.add_contact('voice', phone, 'legislature')
  if photo_url:
    p.image = photo_url

  return p


def mayor_data(node):
  name = node.xpath('string(.//strong)')[6:]
  phone = node.xpath('string(.//p[2]/text()[1])')
  email = node.xpath('string((.//a)[1])')
  photo_url = node.xpath('string(.//img/@src)')

  p = Person(name=name, district='Hamilton', role='Mayor')
  p.add_source(COUNCIL_PAGE)
  p.add_contact('email', email, None)
  p.add_contact('voice', phone, 'legislature')
  p.image = photo_url

  return p
