# coding: utf-8
from __future__ import unicode_literals
from pupa.scrape import Scraper

import re

from utils import lxmlize, CanadianPerson as Person

COUNCIL_PAGE = 'http://nslegislature.ca/index.php/people/members/'

PARTIES = {
    'Liberal': 'Nova Scotia Liberal Party',
    'PC': 'Progressive Conservative Association of Nova Scotia',
    'NDP': 'Nova Scotia New Democratic Party',
    'I': 'Independent'
}


def get_party(abbreviation):
  """Return a political party based on party abbreviation"""
  return PARTIES[abbreviation]


class NovaScotiaPersonScraper(Scraper):

  def scrape(self):
    page = lxmlize(COUNCIL_PAGE)
    for row in page.xpath('//div[@id="content"]/table/tbody/tr'):
      full_name, party_abbr, post = row.xpath('./td//text()')[:3]
      name = ' '.join(reversed(full_name.split(',')))
      detail_url = row[0][0].attrib['href']
      image, phone, email = get_details(detail_url)
      p = Person(name=name, district=post, role='MLA',
                     party=get_party(party_abbr), image=image)
      p.add_source(COUNCIL_PAGE)
      p.add_source(detail_url)
      if phone:
        p.add_contact('voice', phone, 'legislature')
      p.add_contact('email', email, None)
      yield p


def get_details(url):
  page = lxmlize(url)
  image = page.xpath('string(//img[@class="portrait"]/@src)')
  try:
    phone = page.xpath('string(//dd[@class="numbers"]/text())').split(': ')[1]
  except IndexError:
    phone = None
  email_js = page.xpath('string(//dd/script)')
  email_addr = process_email(email_js)
  return image, phone, email_addr


def process_email(js):
  charcodes = reversed(re.findall(r"]='(.+?)'", js))

  def convert_char(code):
    try:
      return chr(int(code))
    except ValueError:
      return code
  content = ''.join(convert_char(code) for code in charcodes)
  return re.search(r'>(.+)<', content).group(1)
