# coding: utf-8
from __future__ import unicode_literals
from pupa.scrape import Scraper

import re

from six.moves.urllib.parse import urljoin

from utils import lxmlize, CanadianPerson as Person

COUNCIL_PAGE = 'http://www.cotesaintluc.org/Administration'


class CoteSaintLucPersonScraper(Scraper):

  def scrape(self):
    page = lxmlize(COUNCIL_PAGE)

    mayor_url = page.xpath('//a[contains(text(), "Mayor")]/@href')[0]
    yield self.scrape_mayor(mayor_url)

    councillors_url = page.xpath('//a[contains(text(), "Councillors")]/@href')[0]
    cpage = lxmlize(councillors_url)

    councillor_rows = cpage.xpath('//tr[td//img]')[:-1]
    for councillor_row in councillor_rows:
      img_cell, info_cell = tuple(councillor_row)
      name = info_cell.xpath(
         'string(.//span[contains(text(), "Councillor")])')[len('Councillor '):]
      district = info_cell.xpath('string(.//p[contains(text(), "District")])')
      email = info_cell.xpath('string(.//a[contains(@href, "mailto:")])')
      if not email:
        email = info_cell.xpath('string(.//strong[contains(text(), "E-mail")]/following-sibling::text())')
      phone = info_cell.xpath(
          'string(.//p[contains(.//text(), "Telephone:")])').split(':')[1]
      img_url_rel = img_cell.xpath('string(//img/@href)')
      img_url = urljoin(councillors_url, img_url_rel)

      p = Person(name=name, district=district, role='Conseiller')
      p.add_source(COUNCIL_PAGE)
      p.add_source(councillors_url)
      p.add_contact('email', email, None)
      p.add_contact('voice', phone, 'legislature')
      p.image = img_url
      yield p

  def scrape_mayor(self, url):
    page = lxmlize(url)
    name = page.xpath(
        'string(//span[contains(text(), "Mayor")])')[len('Mayor '):]

    email = page.xpath('.//a[contains(@href, "mailto:")]/text()')[0]
    phone = page.xpath('//table[1]/tbody/tr/td[1]/p[last()]/text()')[2].replace('Telephone: ', '')

    p = Person(name=name, district='Côte-Saint-Luc', role='Maire')
    p.add_source(COUNCIL_PAGE)
    p.add_source(url)
    p.image = page.xpath('.//img/@src')[0]
    p.add_source(url)
    p.add_contact('email', email, None)
    p.add_contact('voice', phone, 'legislature')
    return p
