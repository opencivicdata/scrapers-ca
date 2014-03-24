# coding: utf-8
from pupa.scrape import Scraper

from utils import lxmlize, CanadianLegislator as Legislator

import re

COUNCIL_PAGE = 'http://www.parl.gc.ca/Parliamentarians/en/members?view=ListAll'


class CanadaPersonScraper(Scraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)
    rows = page.xpath('//div[@class="main-content"]//tr')[1:]
    for row in rows:
      name_cell = row.xpath('./td[1]')[0]
      last_name = name_cell.xpath('.//span[2]/text()')[0]
      first_name = name_cell.xpath('.//span[1]/text()')[0]
      name = u'%s %s' % (first_name, last_name)
      constituency = row.xpath('string(./td[2])')
      province = row.xpath('string(./td[3])')
      party = row.xpath('string(./td[4])')

      mp_page = lxmlize(name_cell.xpath('string(.//a/@href)'))
      email = mp_page.xpath('string(//span[@class="caucus"]/'
                            'a[contains(., "@")])')
      phone = mp_page.xpath('string(//div[@class="hilloffice"]/'
                            'span[contains(., "Telephone")])').split(': ')[1]
      photo = mp_page.xpath('string(//div[@class="profile overview header"]//'
                            'img/@src)')

      m = Legislator(name=name, post_id=constituency, role='MP', chamber='lower', party=party)
      m.add_source(COUNCIL_PAGE)
      m.add_contact('email', email, None)
      m.add_contact('voice', phone, 'legislature')
      m.image = photo
      yield m

