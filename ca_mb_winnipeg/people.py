# coding: utf-8
from __future__ import unicode_literals
from pupa.scrape import Scraper

import re

from six.moves.urllib.parse import urljoin

from utils import lxmlize, CanadianPerson as Person

COUNCIL_PAGE = 'http://winnipeg.ca/council/'


class WinnipegPersonScraper(Scraper):

  def scrape(self):
    page = lxmlize(COUNCIL_PAGE)
    nodes = page.xpath('//td[@width="105"]')
    for node in nodes:
      url = urljoin(COUNCIL_PAGE, node.xpath('string(.//a/@href)'))
      ward = re.search('([A-Z].+) Ward', node.xpath('string(.//a)')).group(1)
      name = ' '.join(node.xpath('string(.//span[@class="k80B"])').split())
      yield councillor_data(url, name, ward)

    mayor_node = page.xpath('//td[@width="315"]')[0]
    mayor_name = mayor_node.xpath('string(./a)')[len('Mayor '):]
    mayor_photo_url = mayor_node.xpath('string(./img/@src)')
    m = Person(name=mayor_name, district='Winnipeg', role='Mayor')
    m.add_source(COUNCIL_PAGE)
    # @see http://www.winnipeg.ca/interhom/mayor/MayorForm.asp?Recipient=CLK-MayorWebMail
    m.add_contact('email', 'CLK-MayorWebMail@winnipeg.ca', None)
    m.image = mayor_photo_url
    yield m


def councillor_data(url, name, ward):
  page = lxmlize(url)
  # email is, sadly, a form
  photo_url = urljoin(url, page.xpath('string(//img[@class="bio_pic"]/@src)'))
  phone = page.xpath('string(//td[contains(., "Phone")]/following-sibling::td)')
  email = (page.xpath('string(//tr[contains(., "Email")]//a/@href)').
           split('=')[1] + '@winnipeg.ca')

  p = Person(name=name, district=ward, role='Councillor')
  p.add_source(COUNCIL_PAGE)
  p.add_source(url)
  p.add_contact('email', email, None)
  p.add_contact('voice', phone, 'legislature')
  p.image = photo_url

  return p
