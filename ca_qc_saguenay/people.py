from pupa.scrape import Scraper

from utils import lxmlize, CanadianLegislator as Legislator

import re
import os
import requests
import tempfile
import shutil

COUNCIL_PAGE = 'http://ville.saguenay.ca/fr/administration-municipale/conseils-municipaux-et-darrondissement/membres-des-conseils'


class SaguenayPersonScraper(Scraper):

  def get_people(self):

    tmpdir = tempfile.mkdtemp()
    page = lxmlize(COUNCIL_PAGE)

    mayor = page.xpath('//div[@class="box"]/p/text()')
    m_name = mayor[0].strip().split('.')[1].strip()
    m_phone = mayor[1].strip().split(':')[1].strip()

    m = Legislator(name=m_name, post_id='Saguenay', role='Maire')
    m.add_source(COUNCIL_PAGE)
    m.add_contact('voice', m_phone, 'legislature')

    yield m

    councillors = page.xpath('//div[@class="box"]//div')
    for councillor in councillors:
      district = councillor.xpath('./h3')[0].text_content().replace('#', '')
      name = councillor.xpath('.//p/text()')[0].replace('M. ', '').replace('Mme ', '').strip()
      phone = councillor.xpath('.//p/text()')[1].split(':')[1].strip().replace(' ', '-')
      email = councillor.xpath('.//a[contains(@href, "mailto:")]')[0].text_content()

      url = councillor.xpath('./p/a')[0].attrib['href']

      p = Legislator(name=name, post_id=district, role='Conseiller')
      p.add_source(COUNCIL_PAGE)

      p.add_contact('voice', phone, 'legislature')
      p.add_contact('email', email, None)
      yield p
