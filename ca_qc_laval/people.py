# coding: utf-8
from __future__ import unicode_literals
from pupa.scrape import Scraper

import re

from utils import lxmlize, CanadianPerson as Person

COUNCIL_PAGE = 'http://www.laval.ca/Pages/Fr/Administration/conseillers-municipaux.aspx'


class LavalPersonScraper(Scraper):

  def scrape(self):
    page = lxmlize(COUNCIL_PAGE)
    for councillor_row in page.xpath('//tr'):
      post = councillor_row.xpath('string(./td[2]/p/text())')
      if post == 'Maire de Laval':
        district = 'Laval'
        role = 'Maire'
      else:
        district = re.sub('^C.?irconscription (?:no )?\d+\D- ', '', post).replace("L'", '').replace(' ', '').replace('bois', 'Bois')
        role = 'Conseiller'
      full_name = councillor_row.xpath('string(./td[2]/p/text()[2])').strip()
      name = ' '.join(full_name.split()[1:])

      phone = councillor_row.xpath(
          'string(.//span[@class="icon-phone"]/following::text())')
      email = councillor_row.xpath(
          'string(.//a[contains(@href, "mailto:")]/@href)')[len('mailto:'):]
      photo_url = councillor_row[0][0].attrib['src']
      p = Person(name=name, district=district, role=role, image=photo_url)
      p.add_source(COUNCIL_PAGE)
      p.add_contact('voice', phone, 'legislature')
      p.add_contact('email', email, None)
      yield p
