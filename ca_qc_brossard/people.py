from pupa.scrape import Scraper, Legislator
from pupa.models import Person
from pupa.models import Organization

from utils import lxmlize

import re

COUNCIL_PAGE = 'http://www.ville.brossard.qc.ca/Ma-ville/conseil-municipal.aspx?lang=en-CA'

class BrossardPersonScraper(Scraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)


    councillors = page.xpath('//a[contains(@href, "mailto:")]')[1:]
    info = councillors[1].xpath('.//parent::div/text()')
    for councillor in councillors:
      name = councillor.text_content()
      email = councillor.attrib['href'].split(':')[1].split('?')[0]
      district = re.sub(r'(?<=[0-9]) (.) (?=S)',', ' , info.pop(0))
      if 'Mayor' in district:
        district = 'brossard'
      phone = info.pop(0).replace('ext. ', 'x').strip()

      p = Legislator(name=name, post_id=district)
      p.add_source(COUNCIL_PAGE)
      p.add_contact('email', email, None)
      p.add_contact('phone', phone, None)
      yield p
