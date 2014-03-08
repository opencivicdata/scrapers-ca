# coding: utf-8
from pupa.scrape import Scraper

from utils import lxmlize, CanadianLegislator as Legislator

import re

COUNCIL_PAGE = 'http://www.london.ca/city-hall/city-council/Pages/default.aspx'
MAYOR_PAGE = 'http://www.london.ca/city-hall/mayors-office/Pages/default.aspx'


class LondonPersonScraper(Scraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)
    councillor_pages = page.xpath('//div[@class="imageLinkContent"]/'
                                  'a[starts-with(text(), "Ward")]/@href')
    for councillor_page in councillor_pages:
      yield councillor_data(councillor_page)

    mayor_page = lxmlize(MAYOR_PAGE)
    mayor_connecting_url = mayor_page.xpath('string(//a[@class="headingLink"]'
      '[contains(text(), "Connecting")]/@href)')
    yield mayor_data(mayor_connecting_url)


def councillor_data(url):
  page = lxmlize(url)

  name = page.xpath('string(//h1[@id="TitleOfPage"])')
  district = page.xpath('string(//h2)')

  # TODO: They seem to give the same address for all councilors. Do we care?
  # TODO: Councillor emails are built with js specifically to prevent scraping.
  # TODO: The JS can be scraped.

  address = page.xpath('string(//div[@class="asideContent"])')

  photo = page.xpath('string(//div[@id="contentright"]//img[1]/@src)')
  phone = get_phone_data(page)

  p = Legislator(name=name, post_id=district, role='Councillor')
  p.add_source(COUNCIL_PAGE)
  p.add_source(url)
  p.add_contact('address', address, 'legislature')
  p.add_contact('phone', phone, 'legislature')
  p.image = photo

  return p

def mayor_data(url):
  page = lxmlize(url)

  name = page.xpath('string(//h1[@id="TitleOfPage"])').split('Mayor')[-1]
  photo = page.xpath('string(//div[@class="imageLeftDiv"]/img/@src)')
  phone = get_phone_data(page)

  p = Legislator(name=name, post_id='London', role='Mayor')
  p.add_source(MAYOR_PAGE)
  p.add_source(url)
  p.image = phone
  return p

def get_phone_data(page):
  # We search for "hone" because the first "p" can change case... oh, xpath.
  # We also only return the first phone number we get. There's no consistency.
  phone_text = page.xpath('string((//span[contains(@class, "contactValue")]'
                          '[contains(text(), "hone")])[1])')
  return re.search(r'[0-9].*$', phone_text).group()
