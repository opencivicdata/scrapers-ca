# coding: utf-8
from pupa.scrape import Scraper

from utils import lxmlize, CanadianLegislator as Legislator

from urlparse import urljoin

import re

COUNCIL_PAGE = 'http://www.cityofkingston.ca/city-hall/city-council/mayor-and-council'


class KingstonPersonScraper(Scraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)
    mayor_and_council_urls = page.xpath('//ul[@class="no-list no-margin"]//'
                                        'ul[@class="no-list no-margin"]//'
                                        'li/a/@href')
    mayor_url = mayor_and_council_urls[0]
    council_urls = mayor_and_council_urls[1:]

    for councillor_url in council_urls:
      yield councillor_data(councillor_url)

    yield mayor_data(mayor_url)

def councillor_data(url):
  page = lxmlize(url)

  # largely based on old scraper
  contact_node = page.xpath('//div[text()[contains(.,"Phone:")]]')[0]

  name = contact_node.xpath('string(./span[1])')
  district = contact_node.xpath('string(./text()[2])')
  email = contact_node.xpath('string(.//a)')
  phone = contact_node.xpath('string(./text()[5])').split(': ')[-1]
  photo_url_rel = contact_node.xpath('string(.//img/@src)')
  photo_url = urljoin(url, photo_url_rel)

  p = Legislator(name=name, post_id=district, role='Councillor')
  p.add_source(COUNCIL_PAGE)
  p.add_source(url)
  p.add_contact('email', email, None)
  p.add_contact('voice', phone, 'legislature')
  p.image = photo_url

  return p

def mayor_data(url):
  page = lxmlize(url)

  # largely based on old scraper
  contact_node = page.xpath('//div[text()[contains(.,"Phone:")]]')[0]

  name = contact_node.xpath('string(./span[1])')
  address = contact_node.xpath('string(.//p)')
  email = contact_node.xpath('string(.//a)')
  phone = contact_node.xpath('string(./text()[3])').split('\n')[1].split(':')[1]
  photo_url_rel = contact_node.xpath('string(.//img/@src)')
  photo_url = urljoin(url, photo_url_rel)

  p = Legislator(name=name, post_id='Kingston', role='Mayor')
  p.add_source(COUNCIL_PAGE)
  p.add_source(url)
  p.add_contact('email', email, None)
  p.add_contact('voice', phone, 'legislature')
  p.add_contact('address', address, 'legislature')
  p.image = photo_url

  return p
