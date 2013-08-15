from pupa.scrape import Scraper, Legislator
from larvae.person import Person
from larvae.organization import Organization

from utils import lxmlize

import re

COUNCIL_PAGE = 'http://www.town.caledon.on.ca/en/townhall/council.asp'

class CaledonPersonScraper(Scraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)

    councillors = page.xpath('//div[@id="printAreaContent"]//table//td')[2:]
    for councillor in councillors:
      district, name = councillor.text_content().split('-')
      url = councillor.xpath('.//a')[0].attrib['href']

      p = Legislator(name=name, post_id=district)
      p.add_source(COUNCIL_PAGE)
      p.add_source(url)

      page = lxmlize(url)

      info = page.xpath('//table[@summary="Councillor"]/tbody/tr/td[2]')[0]
      info = info.text_content().strip().splitlines(True)
      info = [x for x in info if not x == u'\xa0\n']
      address = info[1]
      email = re.findall(r'[a-z]+.[a-z]+@caledon.ca', info[2])[0]
      numbers = re.findall(r'[0-9]{3}.[0-9]{3}. ?[0-9]{4}', info[2])
      phone = numbers[0]
      fax = numbers[1]

      p.add_contact('address', address, None)
      p.add_contact('email', email, None)
      p.add_contact('phone', phone, None)
      p.add_contact('fax', fax, None)

      yield p