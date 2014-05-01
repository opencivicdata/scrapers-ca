# coding: utf-8
from pupa.scrape import Scraper

from utils import lxmlize, CanadianLegislator as Legislator

import re

COUNCIL_PAGE = 'http://www.ville.brossard.qc.ca/Ma-ville/conseil-municipal.aspx?lang=en-CA'


class BrossardPersonScraper(Scraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)

    councillors = page.xpath('//a[contains(@href, "mailto:")]')[1:]
    info = councillors[1].xpath('.//parent::div/text()')
    print info
    for num, councillor in enumerate(councillors):
      name = councillor.text_content()
      if u'Ã©' in name:
        name = name.encode('iso-8859-1').decode('utf-8')
      email = councillor.attrib['href'].split(':')[1].split('?')[0]
      district = re.sub(r'(?<=[0-9]).+', '', info.pop(0)).strip()
      role = 'Conseiller'
      if 'Mayor' in district:
        district = 'Brossard'
        role = 'Maire'
      phone = info.pop(0).replace('ext. ', 'x').strip()

      p = Legislator(name=name, post_id=district, role=role)
      p.add_source(COUNCIL_PAGE)

      image = page.xpath('//div[@class="slide_wrap"]//a[@class="slide item-%d"]/@style' % num)[0]
      p.image = re.findall(r'\((.*)\)', image)[0]

      p.add_contact('email', email, None)
      p.add_contact('voice', phone, 'legislature')
      yield p
