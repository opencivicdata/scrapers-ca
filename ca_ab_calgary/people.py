# coding: utf-8
from pupa.scrape import Scraper

from utils import lxmlize, CanadianLegislator as Legislator

import re
from urlparse import ulrjoin

COUNCIL_PAGE = 'http://www.calgary.ca/General/Pages/Calgary-City-Council.aspx'


class CalgaryPersonScraper(Scraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)
    councillor_urls = page.xpath('//div[@class="cocis-image"]/a/@href')
    for url in councillor_urls:
      yield councillor_data(urljoin(COUNCIL_PAGE, url))

def councillor_data(url):
  page = lxmlize(url)
  name_and_ward = page.xpath('string(//h1[@id="cocis-content-page-title"])')
  ward, name = re.match(r'(Ward [0-9]+) Councillor (.+)').groups()
  photo_url_rel = page.xpath('div[@id="contactInfo"]//img[1]/@src')
  photo_url = urljoin(url, photo_url_rel)
  # no email, there's a contact form!
  phone = page.xpath('//strong[contains(., "Phone")]/next-sibling::text()')

  p = Legislator(name=name, post_id=ward, role='Councillor')
  p.add_source(COUNCIL_PAGE)
  p.add_contact('voice', phone, 'legislature')
  p.image = photo

  return p

