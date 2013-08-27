from pupa.scrape import Scraper, Legislator

from utils import lxmlize, CanadianScraper

import re
import os
import requests
import tempfile
import shutil

COUNCIL_PAGE = 'http://ville.saguenay.ca/fr/administration-municipale/conseils-municipaux-et-darrondissement/membres-des-conseils'


class SaguenayPersonScraper(CanadianScraper):

  def get_people(self):

    tmpdir = tempfile.mkdtemp()
    page = lxmlize(COUNCIL_PAGE)
    organization = self.get_organization()
    yield organization

    mayor = page.xpath('//div[@class="box"]/p/text()')
    m_name = mayor[1].strip().split('.')[1].strip()
    m_phone = mayor[2].strip().split(':')[1].strip()

    m = Legislator(name=m_name, post_id='Saguenay')
    m.add_source(COUNCIL_PAGE)
    m.add_membership(organization, role='mayor')
    m.add_contact('phone', m_phone, 'office')
    m.image = page.xpath('//div[@class="box"]/p/img/@src')[0]

    yield m

    councillors = page.xpath('//div[@class="box"]//div')
    for councillor in councillors:
      district = councillor.xpath('./h3')[0].text_content()
      name = councillor.xpath('.//p/text()')[1].replace('M. ', '').replace('Mme ', '').strip()

      phone = councillor.xpath('.//p/text()')[2].split(':')[1].strip().replace(' ', '-')
      email = councillor.xpath('.//a[contains(@href, "mailto:")]')[0].text_content()

      url = councillor.xpath('./p/a')[0].attrib['href']

      p = Legislator(name=name, post_id=district)
      p.add_source(COUNCIL_PAGE)
      p.add_source(url)
      p.add_membership(organization, role='councillor')

      p.image = councillor.xpath('./p/img/@src')[0]

      p.add_contact('phone', phone, 'office')
      p.add_contact('email', email, None)
      yield p
