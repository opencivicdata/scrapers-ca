# coding: utf-8
from pupa.scrape import Scraper

from utils import lxmlize, CanadianLegislator as Legislator

import re
from urlparse import urljoin

COUNCIL_PAGE = 'http://www.victoria.ca/EN/main/city/mayor-council-committees/councillors.html'


class VictoriaPersonScraper(Scraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)
    nodes = page.xpath('(//div[@id="main"]//ul)[1]/li')
    for node in nodes:
      url = urljoin(COUNCIL_PAGE, node.xpath('string(./a/@href)'))
      name = node.xpath('string(./a)')
      yield councillor_data(url, name, 'Councillor')

    mayor_node = page.xpath('//a[contains(text(), "Mayor")][1]')[0]
    mayor_url = urljoin(COUNCIL_PAGE, mayor_node.xpath('string(./@href)'))
    mayor_name = mayor_node.xpath('string(.)')
    yield councillor_data(url, mayor_name, 'Mayor')

def councillor_data(url, name, role):
  page = lxmlize(url)
  email = page.xpath('string(//a[contains(@href, "mailto")])')
  phone_str = page.xpath('string(//div[@id="content"]//strong[1]/'
                         'following-sibling::text()[contains(., "Phone")])')
  phone = phone_str.split(':')[1]
  photo_url = urljoin(url, 
      page.xpath('string(//div[@id="content"]//img[1]/@src)'))


  # TODO: should post_id be "Nieghborhood Liaison"?
  m = Legislator(name=name, post_id='Victoria', role=role)
  m.add_source(COUNCIL_PAGE)
  m.add_source(url)
  m.add_contact('email', email, None)
  m.add_contact('voice', phone, 'legislature')
  m.image = photo_url
  return m

