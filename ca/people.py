# coding: utf-8
from pupa.scrape import Scraper

from utils import lxmlize, CanadianLegislator as Legislator

import re

COUNCIL_PAGE = 'http://www.parl.gc.ca/Parliamentarians/en/members?view=ListAll'


class CanadaPersonScraper(Scraper):
  """
  The CSV at http://www.parl.gc.ca/Parliamentarians/en/members/export?output=CSV
  accessible from http://www.parl.gc.ca/Parliamentarians/en/members has no
  contact information or photo URLs.
  """

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)
    rows = page.xpath('//div[@class="main-content"]//tr')[1:]
    for row in rows:
      name_cell = row.xpath('./td[1]')[0]
      last_name = name_cell.xpath('string(.//span[1])')
      first_name = name_cell.xpath('string(.//span[2])')
      name = '%s %s' % (first_name, last_name)
      constituency = row.xpath('string(./td[2])')
      province = row.xpath('string(./td[3])')
      party = row.xpath('string(./td[4])')

      url = name_cell.xpath('string(.//a/@href)')
      mp_page = lxmlize(url)
      email = mp_page.xpath('string(//span[@class="caucus"]/'
                            'a[contains(., "@")])')
      phone = mp_page.xpath('string(//div[@class="hilloffice"]/'
                            'span[contains(., "Telephone")])').split(': ')[1]
      photo = mp_page.xpath('string(//div[@class="profile overview header"]//'
                            'img/@src)')

      m = Legislator(name=name, post_id=constituency, role='MP', chamber='lower', party=party)
      m.add_source(COUNCIL_PAGE)
      m.add_source(url)
      m.add_contact('email', email, None)
      m.add_contact('voice', phone, 'legislature')
      m.image = photo
      yield m
