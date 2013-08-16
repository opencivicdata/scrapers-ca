from pupa.scrape import Scraper, Legislator
from larvae.person import Person
from larvae.organization import Organization

from utils import lxmlize

import re

COUNCIL_PAGE = 'http://www.countygp.ab.ca/EN/main/government/council.html'

class GrandePrairieCountyNo1PersonScraper(Scraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)

    councillors = page.xpath('//table[@class="table-plain"]/tbody/tr/td[2]')
    for councillor in councillors:
      name = councillor.xpath('./h2')[0].text_content().split('Division')[0]
      district = re.findall(r'(Division [0-9])', councillor.xpath('./h2')[0].text_content())[0]

      p = Legislator(name=name, post_id=district)
      p.add_source(COUNCIL_PAGE)

      address = councillor.xpath('./p[1]')[0].text_content()
      email = councillor.xpath('.//a[contains(@href, "mailto:")]')[0].text_content()

      p.add_contact('address', address, None)
      p.add_contact('email', email, None)

      numbers = councillor.xpath('./p[2]')[0].text_content().replace('Email: ','').replace(email,'').split(':')
      for index, number in enumerate(numbers):
        if index == 0:
          continue
        contact_type = re.findall(r'[A-Za-z]+', numbers[index-1])[0]
        number = re.findall(r'[0-9]{3}.[0-9]{3}.[0-9]{4}', number)[0].replace('.','-')
        if contact_type == 'Fax':
          p.add_contact('fax', number, None)
        else:
          p.add_contact('phone', number, contact_type)
      yield p
