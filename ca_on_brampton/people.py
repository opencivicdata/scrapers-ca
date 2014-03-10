# coding: utf-8
from pupa.scrape import Scraper

from utils import lxmlize, CanadianLegislator as Legislator

import re

COUNCIL_PAGE = 'http://www.brampton.ca/en/City-Hall/CouncilOffice/Pages/Welcome.aspx'
MAYOR_PAGE = 'http://www.brampton.ca/EN/City-Hall/Office-Mayor/Pages/Welcome.aspx'


class BramptonPersonScraper(Scraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)
    councillor_divs = page.xpath('//div[@class="councillorCard"]');
    for councillor_div in councillor_divs:
      yield councillor_data(councillor_div)

    mayor_page = lxmlize(MAYOR_PAGE)
    yield mayor_data(mayor_page)


def councillor_data(html):
  name = html.xpath('string(./div[@class="councillorInfo"]/a/text()[2])')
  email = html.xpath('string(./div[@class="emailInfo"])')
  district, phone = html.xpath('./div[@class="wardInfo"]/text()')
  photo = html.xpath('string((.//@src)[1])')

  p = Legislator(name=name, post_id=district, role='Councillor')
  p.add_source(COUNCIL_PAGE)
  p.add_contact('voice', phone, 'legislature')
  p.add_contact('email', email, None)
  p.image = photo

  return p

def mayor_data(page):
  # Strip the word "mayor" from the beginning of the photo lavel
  photo_node = page.xpath('//img[@class="mayorsPic"]')[0]
  name = photo_node.xpath('string(./@alt)')[6:]
  photo_url = page.xpath('string(./@src)')

  address_node = page.xpath('//div[@class="address"]')[0]
  email = address_node.xpath('string(.//a)')
  address = ''.join(address_node.xpath('./p/text()')[:3])
  phone = address_node.xpath('string(./p/text()[4])')

  p = Legislator(name=name, post_id='Brampton', role='Mayor')
  p.add_source(MAYOR_PAGE)
  p.add_contact('voice', phone, 'legislature')
  p.add_contact('address', address, 'legislature')
  p.add_contact('email', email, None)
  p.image = photo_url
  print name
  print email
  print address
  print phone
  print photo_url
  return p

