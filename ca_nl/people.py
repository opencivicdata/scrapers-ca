# coding: utf-8
from pupa.scrape import Scraper

from utils import lxmlize, CanadianLegislator as Legislator

import re

COUNCIL_PAGE = 'http://www.assembly.nl.ca/members/cms/membersdirectlines.htm'


class NewfoundlandAndLabradorPersonScraper(Scraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)
    for row in page.xpath('//table[not(@id="footer")]/tr')[1:]:
      name, district, _, email = [cell.xpath('string(.)') for cell in row]
      phone = row[2].xpath('string(text()[1])')
      try:
        photo_page_url = row[0].xpath('./a/@href')[0]
      except IndexError:
        continue # there is a vacant district
      photo_page = lxmlize(photo_page_url)
      photo_url = photo_page.xpath('string(//table//img/@src)')
      district = district.replace(' - ', u'—')  # m-dash
      p = Legislator(name=name, post_id=district, role='MHA', image=photo_url)
      p.add_source(COUNCIL_PAGE)
      p.add_source(photo_page_url)
      p.add_contact('email', email, None)
      # TODO: either fix phone regex or tweak phone value
      p.add_contact('voice', phone, 'legislature')
      yield p

