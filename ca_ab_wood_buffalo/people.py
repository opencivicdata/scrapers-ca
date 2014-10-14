from __future__ import unicode_literals
from pupa.scrape import Scraper

import re

from six.moves.urllib.parse import urljoin

from utils import lxmlize, CanadianPerson as Person

COUNCIL_PAGE = 'http://www.woodbuffalo.ab.ca/Municipal-Government/Mayor-and-Council/Councillor-Profiles.htm'


class WoodBuffaloPersonScraper(Scraper):

  def scrape(self):
    page = lxmlize(COUNCIL_PAGE)

    mayor_url = page.xpath('//li[@id="pageid1075"]/div/a/@href')[0]
    yield scrape_mayor(mayor_url)

    wards = page.xpath('//b')
    for ward in wards:
      ward_name = ward.text_content()
      councillor_links = ward.xpath('./parent::p/a')
      for councillor_link in councillor_links:
        name = councillor_link.text
        p = Person(name=name, post_id=ward_name, role='Councillor')
        url = councillor_link.attrib['href']
        p.add_source(COUNCIL_PAGE)
        p.add_source(url)
        cpage = lxmlize(url)
        image_url_rel = cpage.xpath('string(//div[@id="content"]/img/@src)')
        image_url = urljoin(url, image_url_rel)
        p.image = image_url

        contacts = page.xpath(
            '//div[@id="content"]//div[@class="block"]/text()')
        for contact in contacts:
          if not re.search(r'[0-9]', contact):
            continue
          if not '(' in contact:
            contact_type = 'T'
          else:
            contact_type, contact = contact.split('(')
          contact = contact.replace(') ', '-').strip()
          if 'T' in contact_type:
            p.add_contact('voice', contact, 'legislature')
          if 'H' in contact_type:
            p.add_contact('voice', contact, 'residence')
          if 'C' in contact_type:
            p.add_contact('cell', contact, 'legislature')
          if 'F' in contact_type:
            p.add_contact('fax', contact, 'legislature')
        email = cpage.xpath(
            '//div[@id="content"]//div[@class="block"]//'
            'a[contains(@href, "mailto:")]')[0].text_content()
        p.add_contact('email', email, None)
        yield p


def scrape_mayor(url):
  page = lxmlize(url)
  name = page.xpath('//h1[@id="pagetitle"]/text()')[0].replace('Mayor', '').strip()
  image = page.xpath('//div[@id="content"]/p[1]/img/@src')[0]
  contact_url = page.xpath('//li[@id="pageid1954"]/a/@href')[0]
  page = lxmlize(contact_url)

  info = page.xpath('//div[@id="content"]/div[@class="block"][2]/p/text()')
  address = ' '.join(info[1:4])
  phone = info[4]
  fax = info[5]

  p = Person(name=name, post_id='Wood Buffalo', role='Mayor')
  p.add_source(url)
  p.add_source(contact_url)
  p.add_contact('address', address, 'legislature')
  p.add_contact('voice', phone, 'legislature')
  p.add_contact('fax', fax, 'legislature')
  p.image = image
  return p
