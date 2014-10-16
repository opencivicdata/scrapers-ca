from __future__ import unicode_literals
from pupa.scrape import Scraper

import re

from utils import lxmlize, CanadianPerson as Person

COUNCIL_PAGE = 'http://www.westmount.org/page.cfm?Section_ID=1&Menu_Item_ID=61'


class WestmountPersonScraper(Scraper):

  def scrape(self):
    page = lxmlize(COUNCIL_PAGE)

    mayor = page.xpath('//td[@class="LeftLinksSectionMenu"]/a')[0]
    name = mayor.text_content().replace('Mayor', '').strip()
    url = mayor.attrib['href']
    mayor_page = lxmlize(url)
    p = Person(name=name, district='Westmount', role='Maire')
    p.add_source(COUNCIL_PAGE)
    p.add_source(url)
    mayor_info = mayor_page.xpath('//div[@style="padding-right:10px;"]/table')[0]
    phone = mayor_info.xpath('.//tr[2]/td[2]')[0].text_content().replace(' ', '-')
    fax = mayor_info.xpath('.//tr[3]/td[2]')[0].text_content().replace(' ', '-')
    email = mayor_info.xpath('.//tr[4]/td[2]')[0].text_content().strip()
    p.add_contact('voice', phone, 'legislature')
    p.add_contact('fax', fax, 'legislature')
    p.add_contact('email', email, None)
    yield p

    councillors = page.xpath('//td[@class="LeftLinksSectionMenu" and contains(@style, "border-bottom-style: dashed;")]/a')
    for i, councillor in enumerate(councillors):
      name = councillor.text_content().strip()
      url = councillor.attrib['href']
      page = lxmlize(url)

      if page.xpath('boolean(.//div[@class="SectionTitle"][2])'):
        district = page.xpath('.//div[@class="SectionTitle"]')[1].text_content().split('-')[0].strip()
      else:
        district = 'District ' + str(i + 1)

      info = page.xpath('.//div[@style="padding-right:10px;"]/table')[0]
      phone = info.xpath('.//tr[2]/td[2]')[0].text_content().replace(' ', '-')
      email = info.xpath('.//tr[3]/td[2]')[0].text_content().strip()
      p = Person(name=name, district=district, role='Conseiller')
      p.add_source(COUNCIL_PAGE)
      p.add_source(url)
      p.image = info.xpath('./ancestor::td//div[not(@id="insert")]/img/@src')[0]
      p.add_contact('voice', phone, 'legislature')
      p.add_contact('email', email, None)
      yield p
