# coding: utf-8
from pupa.scrape import Scraper

from utils import lxmlize, CanadianLegislator as Legislator

import re

COUNCIL_PAGE = 'http://www.burnaby.ca/Our-City-Hall/Mayor---Council/Council-Profiles.html'


class BurnabyPersonScraper(Scraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)

    for person_url in page.xpath('//h4/a/@href'):
      yield scrape_person(person_url)

def scrape_person(url):
  page = lxmlize(url)

  role, name = page.xpath('string(//title)').split(' ', 1)
  photo_url = page.xpath('string(//div[@id="content"]//img[@style]/@src)')
  email = page.xpath('string(//a[contains(@href, "mailto:")])')
  phone = page.xpath('string(//li[contains(text(), "Phone:")])')

  p = Legislator(name=name, post_id='Burnaby', role=role, image=photo_url)
  p.add_source(COUNCIL_PAGE)
  p.add_source(url)
  p.add_contact('email', email, None)
  if phone:
    p.add_contact('voice', phone, 'legislature')
  return p

