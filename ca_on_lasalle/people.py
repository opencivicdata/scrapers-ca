from __future__ import unicode_literals
from pupa.scrape import Scraper

import re

from utils import lxmlize, CanadianPerson as Person

COUNCIL_PAGE = 'http://www.town.lasalle.on.ca/Council/council-council.htm'


class LaSallePersonScraper(Scraper):

  def scrape(self):
    page = lxmlize(COUNCIL_PAGE)

    councillors = page.xpath('//div[@align="center" and not(@class="background")]//td/p')
    for councillor in councillors:
      if not councillor.text_content().strip():
        continue
      name = councillor.xpath('./font/b/text()')
      if not name:
        name = councillor.xpath('./font/text()')
      if 'e-mail' in name[0]:
        name = councillor.xpath('./b/font/text()')
      name = name[0]
      role = 'Councillor'
      if 'Mayor' in name:
        name = name.replace('Mayor', '')
        role = 'Mayor'

      p = Person(name=name, district="LaSalle", role=role)
      p.add_source(COUNCIL_PAGE)

      photo_url = councillor.xpath('./parent::td//img/@src')[0]
      p.image = photo_url

      email = councillor.xpath('.//a[contains(@href, "mailto:")]/text()')[0]
      p.add_contact('email', email, None)

      phone = re.findall(r'(?<=phone:)(.*)(?=home)', councillor.text_content(), flags=re.DOTALL)
      if phone:
        p.add_contact('voice', phone[0].strip(), 'legislature')

      home_phone = re.findall(r'(?<=home phone:)(.*)', councillor.text_content(), flags=re.DOTALL)[0]
      p.add_contact('voice', home_phone.strip(), 'residence')
      yield p
