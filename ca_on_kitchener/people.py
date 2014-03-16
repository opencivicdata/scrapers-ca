# coding: utf-8
from pupa.scrape import Scraper

from utils import lxmlize, CanadianLegislator as Legislator

from urlparse import urljoin

import re

COUNCIL_PAGE = 'http://www.kitchener.ca/en/insidecityhall/WhoIsMyCouncillor.asp'
MAYOR_PAGE = 'http://www.kitchener.ca/en/insidecityhall/MayorSLandingPage.asp'


class KitchenerPersonScraper(Scraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)

    councillor_urls = page.xpath('//div[@id="printArea"]//li/a/@href')

    for councillor_url in councillor_urls:
      cd = councillor_data(councillor_url)
      if cd: # see below about rep page with no ward
        yield cd

    yield mayor_data(MAYOR_PAGE)

def councillor_data(url):
  page = lxmlize(url)

  infobox_node = page.xpath('//div[@id="printArea"]')[0]
  name = infobox_node.xpath('string(.//h1[1])')[len('Councillor'):]
  district = infobox_node.xpath('string(.//h2[contains(., "Ward")])')

  contact_node = infobox_node.xpath('.//p[contains(text(), "Coun.")]')[0]
  email = contact_node.xpath('string(.//text()[contains(., "@")])').split()[-1]

  # TODO: contact details are tricky
  #address = '\n'.join(contact_node.xpath('./text()')[:4])
  #phone = contact_node.xpath('string(./text()[5])').strip('City hall:')
  
  photo_url_rel = page.xpath('string(//div[@id="sideBar"]//img/@src)')
  photo_url = urljoin(COUNCIL_PAGE, photo_url_rel)

  # if statement below because one rep page doesn't list ward:
  # http://www.kitchener.ca/en/insidecityhall/Yvonne.asp
  if district:
    p = Legislator(name=name, post_id=district, role='Councillor')
    p.add_source(COUNCIL_PAGE)
    p.add_source(url)
    if email:
      p.add_contact('email', email, None)
    p.image = photo_url

    return p

def mayor_data(url):
  page = lxmlize(url)

  infobox_node = page.xpath('//div[@id="printArea"]')[0]
  name = infobox_node.xpath('string(.//h1)')[6:] # strip 'Mayor' prefix

  contact_node = page.xpath('//div[@id="contentIntContact"]')[0]

  # TODO: fruitlessly wasted way too much time below
  address = '\n'.join(contact_node.xpath('./p[2]/text()')[:3])
  phone = contact_node.xpath('string(./p[2]/text()[contains(., "T.")])')[3:]

  photo_url_rel = page.xpath('string(//div[@id="sideBar"]//img/@src)')
  photo_url = urljoin(COUNCIL_PAGE, photo_url_rel)

  p = Legislator(name=name, post_id='Kitchener', role='Mayor')
  p.add_source(url)
  p.image = photo_url

  return p

