from pupa.scrape import Scraper, Legislator
from larvae.person import Person
from larvae.organization import Organization

from utils import lxmlize

import re

COUNCIL_PAGE = 'http://www.westmount.org/page.cfm?Section_ID=1&Menu_Item_ID=61'

class WestmountPersonScraper(Scraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)

    mayor = page.xpath('//td[@class="LeftLinksSectionMenu"]/a')[0]
    name = mayor.text_content().replace('Mayor','').strip()
    url = mayor.attrib['href']
    mayor_page = lxmlize(url)
    p = Legislator(name=name, district='Westmount')
    p.add_source(COUNCIL_PAGE)
    p.add_source(url)
    mayor_info = mayor_page.xpath('//div[@style="padding-right:10px;"]/table')[0]
    phone = mayor_info.xpath('.//tr[2]/td[2]')[0].text_content().replace(' ','-')
    fax = mayor_info.xpath('.//tr[3]/td[2]')[0].text_content().replace(' ','-')
    email = mayor_info.xpath('.//tr[4]/td[2]')[0].text_content().strip()
    p.add_contact('phone', phone, None)
    p.add_contact('fax', fax, None)
    p.add_contact('email', email, None)
    yield p

    councillors = page.xpath('//td[@class="LeftLinksSectionMenu" and contains(@style, "border-bottom-style: dashed;")]/a')
    for councillor in councillors:
      name = councillor.text_content().strip()
      url = councillor.attrib['href']
      page = lxmlize(url)
      district = page.xpath('.//div[@class="SectionTitle"]')[1].text_content().split('-')[0].strip()
      info = page.xpath('.//div[@style="padding-right:10px;"]/table')[0]
      phone = info.xpath('.//tr[2]/td[2]')[0].text_content().replace(' ','-')
      email = info.xpath('.//tr[3]/td[2]')[0].text_content().strip()
      p = Legislator(name=name, district=district)
      p.add_source(COUNCIL_PAGE)
      p.add_source(url)
      p.add_contact('phone', phone, None)
      p.add_contact('email', email, None)
      yield p