# coding: utf-8
from pupa.scrape import Scraper

from utils import lxmlize, CanadianLegislator as Legislator

import re

COUNCIL_PAGE = 'http://www.surrey.ca/city-government/2999.aspx'


class SurreyPersonScraper(Scraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)
    councillor_links = page.xpath(
      '//div[@class="inner-wrapper"]//a[contains(text(), "Councillor")]')
    for link in councillor_links:
      role, name = link.text.split(' ', 1)
      url = link.attrib['href']
      councillor_page = lxmlize(url)
      photo_url = councillor_page.xpath(
          'string(.//div[@class="inner-wrapper"]/p/img/@src)')
      phone = councillor_page.xpath(
          'string(//text()[contains(., "hone:")][1])')
      email = councillor_page.xpath(
          'string(//a[contains(@href, "mailto:")])')

      p = Legislator(name=name, post_id='Surrey', role=role, image=photo_url)
      p.add_source(COUNCIL_PAGE)
      p.add_source(url)
      if phone:
          p.add_contact('voice', phone, 'legislature')
      p.add_contact('email', email, None)
      yield p

    mayor_link = page.xpath(
        '//div[@class="inner-wrapper"]//a[contains(text(), "Mayor")]')[0]
    mayor_url = mayor_link.attrib['href']
    name = mayor_link.text.split(' ', 2)[1]
    mayor_page = lxmlize(mayor_url)
    photo_url = mayor_page.xpath('string(//img[contains(@src, "Mayor")]/@src)')
    phone = mayor_page.xpath('string(//text()[contains(., "Office:")])')
    # no email

    p = Legislator(name=name, post_id='Surrey', role='Mayor', image=photo_url)
    p.add_source(COUNCIL_PAGE)
    p.add_source(mayor_url)
    p.add_contact('voice', phone, 'legislature')
    yield p
