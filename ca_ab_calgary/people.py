# coding: utf-8
from pupa.scrape import Scraper

from utils import lxmlize, CanadianLegislator as Legislator

import re
from urlparse import urljoin

COUNCIL_PAGE = 'http://www.calgary.ca/General/Pages/Calgary-City-Council.aspx'
MAYOR_PAGE = 'http://calgarymayor.ca/forms_all.php'


class CalgaryPersonScraper(Scraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)
    nodes = page.xpath('//div[contains(@class,"cocis-has-caption")]')[1:]
    for node in nodes:
      url = urljoin(COUNCIL_PAGE, node.xpath('string(.//a[1]/@href)'))
      name = node.xpath('string(.//a//text())')
      ward = ' '.join(node.xpath('string(.//strong)').split()[:-1])
      yield councillor_data(url, name, ward)

    mayor_node = page.xpath('//div[contains(@class, "cocis-image-panel")]')[0]
    photo_url = urljoin(COUNCIL_PAGE, mayor_node.xpath('string(.//img/@src)'))
    name = mayor_node.xpath('string(.//a//text())')
    mayor_page = lxmlize(MAYOR_PAGE)
    email = mayor_page.xpath('string(//a[contains(., "@")])')
    phone = mayor_page.xpath('string(//strong[contains(., "Phone")]/'
                             'following-sibling::text())')
    m = Legislator(name=name, post_id='Calgary', role='Mayor')
    m.add_source(COUNCIL_PAGE)
    m.add_source(MAYOR_PAGE)
    m.add_contact('email', email, None)
    m.add_contact('voice', phone, 'legislature')
    m.image = photo_url
    yield m

def councillor_data(url, name, ward):
  page = lxmlize(url)
  photo_url_rel = page.xpath('string(//div[@id="contactInfo"]//img[1]/@src)')
  photo_url = urljoin(url, photo_url_rel)
  # no email, there's a contact form!
  phone = page.xpath('string(//p[contains(./strong, "Phone")]/text())').strip()

  p = Legislator(name=name, post_id=ward, role='Councillor')
  p.add_source(COUNCIL_PAGE)
  if phone:
    p.add_contact('voice', phone, 'legislature')
  p.image = photo_url

  return p

