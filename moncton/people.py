from pupa.scrape import Scraper, Legislator
from larvae.person import Person
from larvae.organization import Organization

from .utils import lxmlize

import re

COUNCIL_PAGE = 'http://www.moncton.ca/Government/City_Council.htm'

class MonctonPersonScraper(Scraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)

    councillors = page.xpath('//td[@class="cityfonts"]')
    for councillor in councillors:
      name = councillor.xpath('.//a')[0].text_content()
      district = councillor.xpath('.//span/text()')[1]

      email = councillor.xpath('.//a')[0].attrib['href'].replace('mailto:','')
      
      url = councillor.xpath('.//a')[-1].attrib['href']
      page = lxmlize(url)

      p = Legislator(name=name, district=district)
      p.add_source(COUNCIL_PAGE)
      p.add_source(url)
      p.add_contact('Email', email, None)

      contact_info = page.xpath('.//table[@class="whiteroundedbox"]//td/p[contains(text()," ")]')[0].text_content()
      phone_nos = re.findall(r'(([0-9]{3}-)?([0-9]{3}-[0-9]{4}))', contact_info)
      for phone in phone_nos:
        p.add_contact('Phone', phone[0], None)  
      yield p   