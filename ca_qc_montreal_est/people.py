# coding: utf-8
from __future__ import unicode_literals
from pupa.scrape import Scraper

import re

from utils import lxmlize, CanadianPerson as Person

COUNCIL_PAGE = 'http://ville.montreal-est.qc.ca/site2/index.php?option=com_content&view=article&id=12&Itemid=59'


class MontrealEstPersonScraper(Scraper):

  def scrape(self):
    page = lxmlize(COUNCIL_PAGE, user_agent='Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)')

    councillors = page.xpath('//table[last()]//tr/td[1]//strong')
    for i, councillor in enumerate(councillors):
      name = councillor.text_content().strip()
      if not name:
        continue
      if 'maire' in name:
        name = name.split('maire')[1].strip()
        district = 'Montréal-Est'
      else:
        district = councillor.xpath('./ancestor::td/following-sibling::td//strong')[-1].text_content()
        district = 'District %s' % re.sub('\D+', '', district)
      email = councillor.xpath('./ancestor::tr/following-sibling::tr//a[contains(@href, "mailto:")]')[0].text_content().strip()
      role = 'Maire' if i == 0 else 'Conseiller'
      p = Person(name=name, district=district, role=role)
      p.add_source(COUNCIL_PAGE)
      p.add_contact('email', email, None)
      yield p
