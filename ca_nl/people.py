# coding: utf-8
from pupa.scrape import Scraper

from utils import lxmlize, CanadianLegislator as Legislator

import re

PARL_URL = 'http://www.assembly.nl.ca/members/cms/membersdirectlines.htm'


class NewfoundlandAndLabradorPersonScraper(Scraper):

  def get_people(self):
    page = lxmlize(PARL_URL)
    for row in page.xpath('//table[1]/tr')[1:]:
      name, district, _, email = [cell.xpath('string(.)') for cell in row]
      phone = row[2].xpath('string(text()[1])')
      try:
        photo_page_url = row[0].xpath('./a/@href')[0]
      except IndexError:
        continue # there is a vacant district
      photo_page = lxmlize(photo_page_url)
      photo_url = photo_page.xpath('string(//table//img/@src)')
      p = Legislator(name=name, post_id=district, role='MHA', image=photo_url)
      p.add_source(PARL_URL)
      p.add_source(photo_page_url)
      p.add_contact('email', email, None)
      # TODO: either fix phone regex or tweak phone value
      p.add_contact('voice', phone, 'legislature')
      yield p

