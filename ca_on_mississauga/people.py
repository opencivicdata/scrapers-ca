# coding: utf-8
from pupa.scrape import Scraper

from utils import lxmlize, CanadianLegislator as Legislator

import re

COUNCIL_PAGE = 'http://www.mississauga.ca/portal/cityhall/mayorandcouncil'
MAYOR_PAGE = 'http://www.mississauga.ca/portal/cityhall/contactthemayor'


class MississaugaPersonScraper(Scraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)

    councillor_urls = page.xpath('//area/@href')[1:]

    for councillor_url in councillor_urls:
      yield councillor_data(councillor_url)

    yield mayor_data(MAYOR_PAGE)


def councillor_data(url):
  page = lxmlize(url)

  name = page.xpath('string(//strong[1]/text())')
  district = page.xpath('string(//span[@class="pageHeader"])')
  email = page.xpath('string(//div[@class="blockcontentclear"]//a/'
                     '@href[contains(., "@")][1])')
  photo = page.xpath('string(//div[@class="blockcontentclear"]//img[1]/@src)')

  p = Legislator(name=name, post_id=district, role='Councillor')
  p.add_source(COUNCIL_PAGE)
  p.add_source(url)
  p.add_contact('email', email, None)
  p.image = photo

  return p

def mayor_data(url):
  page = lxmlize(url)

  # TODO: Consider getting photo. It's on a separate page.
  name_text = page.xpath('//p[contains(text(), "Worship Mayor")]/text()')[0]
  name = ' '.join(name_text.split()[3:]) # TODO: probably too brittle
  email = page.xpath('//a[contains(@href, "mailto")]/text()')[0]

  p = Legislator(name=name, post_id='Mississauga', role='Mayor')
  p.add_source(url)
  p.add_contact('email', email, None)

  return p

