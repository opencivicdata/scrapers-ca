# coding: utf-8
from pupa.scrape import Scraper

from utils import lxmlize, CanadianLegislator as Legislator

import re

COUNCIL_PAGE = 'http://www.abbotsford.ca/mayorcouncil/city_council/email_mayor_and_council.htm'

MAYOR_URL = 'http://www.abbotsford.ca/mayorcouncil/city_council/mayor_banman.htm'

class AbbotsfordPersonScraper(Scraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)
    councillor_links = page.xpath('//li[@id="pageid2117"]/ul/li/a')[2:10]
    for link in councillor_links:
      if not link.text.startswith('Councillor'):
        continue
      url = link.attrib['href']
      page = lxmlize(url)
      mail_link = page.xpath('//a[@title]')[0]
      name = mail_link.attrib['title']
      email = mail_link.attrib['href'][len('mailto:'):]
      photo_url = page.xpath('string(//div[@class="pageContent"]//img[@align="right"]/@src)')
      p = Legislator(name=name, post_id='Abbotsford', role='Councillor',
                     image=photo_url)
      p.add_source(url)
      p.add_contact('email', email, None)
      yield p

    page = lxmlize(MAYOR_URL)
    name = page.xpath('string(//h1)').split(' ', 1)[1]
    photo_url = page.xpath('string(//img[@hspace=10]/@src)')
    # email is hidden behind a form
    p = Legislator(name=name, post_id='Abbotsford', role='Mayor', image=photo_url)
    p.add_source(MAYOR_URL)
    yield p

