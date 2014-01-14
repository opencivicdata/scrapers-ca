# coding: utf8
from pupa.scrape import Scraper, Legislator

from utils import lxmlize

import re

COUNCIL_PAGE = 'http://ville.montreal-est.qc.ca/site2/index.php?option=com_content&view=article&id=12&Itemid=59'


class MontrealEstPersonScraper(Scraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)

    councillors = page.xpath('//table[@width="455"]//tr/td[1]//strong')
    for i, councillor in enumerate(councillors):
      name = councillor.text_content().strip()
      if not name:
        continue
      if 'maire' in name:
        name = name.split('maire')[1].strip()
        district = u'Montréal-Est'
      else:
        district = councillor.xpath('./ancestor::td/following-sibling::td//strong')[-1].text_content()
        district = ' '.join(district.split()[1:])
      email = councillor.xpath('./ancestor::tr/following-sibling::tr//a[contains(@href, "mailto:")]')[0].text_content().strip()
      role = 'Mayor' if i == 0 else 'Councillor'
      p = Legislator(name=name, post_id=district, role=role)
      p.add_source(COUNCIL_PAGE)
      p.add_contact('email', email, None)
      yield p
