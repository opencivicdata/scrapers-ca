# coding: utf-8
from pupa.scrape import Scraper

from utils import lxmlize, CanadianLegislator as Legislator

import re
from urlparse import urljoin

COUNCIL_PAGE = 'http://regina.ca/residents/council-committees/meet-city-council/'
MAYOR_CONTACT_URL = 'http://www.regina.ca/residents/regina-mayor/contact_mayor'


class ReginaPersonScraper(Scraper):

  def get_people(self):
    root = lxmlize(COUNCIL_PAGE)

    councillor_links = root.xpath('//div[@id="right_col"]//'
                                  'li[contains(., "Ward")]/a')
    for link in councillor_links:
      text = link.xpath('string(.)')
      ward, name = text.split(' - Councillor ')
      url = link.xpath('string(./@href)')
      yield councillor_data(url, name, ward)

    mayor_link = root.xpath('//div[@id="right_col"]//'
                            'li[contains(., "Mayor")]/a')[0]
    mayor_name = mayor_link.xpath('string(.)')[len('Mayor '):]
    mayor_url = mayor_link.xpath('string(./@href)')
    yield mayor_data(mayor_url, mayor_name)

def councillor_data(url, name, ward):
  page = lxmlize(url)
  # sadly, email is a form on a separate page
  phone = page.xpath('string(//strong[contains(., "Phone")])').split(':')[1]
  photo_url = urljoin(url, 
      page.xpath('(div[@id="contentcontainer"]//img)[2]/@src'))
  m = Legislator(name=name, post_id=ward, role='Councillor')
  m.add_source(COUNCIL_PAGE)
  m.add_source(url)
  m.add_contact('voice', phone, 'legislature')
  m.image = photo_url
  yield m


def mayor_data(url, name):
  page = lxmlize(url)
  photo_url = urljoin(url, 
      page.xpath('string((//div[@id="contentcontainer"]//img)[1]/@src)'))
  contact_page = lxmlize(MAYOR_CONTACT_URL)
  email = contact_page.xpath('string(//a[contains(., "@")][1])')

  m = Legislator(name=name, post_id='Regina', role='Mayor')
  m.add_source(COUNCIL_PAGE)
  m.add_source(url)
  m.add_source(MAYOR_CONTACT_URL)
  m.add_contact('email', email, None)
  m.image = photo_url

  return m

