# coding: utf-8
from pupa.scrape import Scraper

from utils import lxmlize, CanadianLegislator as Legislator

import re

COUNCIL_PAGE = 'http://www.ontla.on.ca/web/members/member_addresses.do'


class OntarioPersonScraper(Scraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)
    for block in page.xpath('//div[@class="addressblock"]'):
      name_elem = block.xpath('.//a[@class="mpp"]')[0]
      name = ' '.join(name_elem.text.split())
      riding = block.xpath(
          'string(.//div[@class="riding"])').replace('--', u'\u2014').replace(u'Chatham—Kent', 'Chatham-Kent') # m-dash to hyphen
      email = block.xpath('string(.//a[contains(@href, "mailto:")])')
      phone = block.xpath('string(.//div[@class="phone"])')
      mpp_url = name_elem.attrib['href']
      mpp_page = lxmlize(mpp_url)
      photo_url = mpp_page.xpath('string(//img[@class="mppimg"]/@src)')
      party = mpp_page.xpath('string(//div[@class="partyaffil"]/h3)')
      p = Legislator(name=name, post_id=riding, role='MPP', 
          party=party, image=photo_url)
      p.add_source(COUNCIL_PAGE)
      p.add_source(mpp_url)
      p.add_contact('email', email, None)
      p.add_contact('voice', phone, 'legislature')
      yield p

