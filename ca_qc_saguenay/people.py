from pupa.scrape import Scraper, Legislator
from larvae.person import Person
from larvae.organization import Organization

from utils import lxmlize

import re, os, requests, tempfile, shutil

COUNCIL_PAGE = 'http://ville.saguenay.ca/fr/administration-municipale/conseils-municipaux-et-darrondissement/membres-des-conseils'

class SaguenayPersonScraper(Scraper):

  def get_people(self):

    tmpdir = tempfile.mkdtemp()
    page = lxmlize(COUNCIL_PAGE)

    mayor = page.xpath('//div[@class="box"]/p/text()')
    m_name = mayor[1].strip().split('.')[1].strip()
    m_phone = mayor[2].strip().split(':')[1].strip()

    m = Legislator(name=m_name, post_id='Saguenay')
    m.add_source(COUNCIL_PAGE)
    m.add_contact('phone', m_phone, None)

    yield m

    councillors = page.xpath('//div[@class="box"]//div')
    for councillor in councillors:
      district = councillor.xpath('./h3')[0].text_content()
      name = councillor.xpath('.//p/text()')[1].replace('M. ','').replace('Mme ','').strip()

      phone = councillor.xpath('.//p/text()')[2].split(':')[1].strip().replace(' ','-')
      email = councillor.xpath('.//a[contains(@href, "mailto:")]')[0].text_content()

      url = councillor.xpath('./p/a')[0].attrib['href']

      p = Legislator(name=name, post_id=district)
      p.add_source(COUNCIL_PAGE)
      p.add_source(url)

      p.add_contact('phone', phone, None)
      p.add_contact('email', email, None)
      yield p