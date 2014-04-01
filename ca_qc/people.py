# coding: utf-8
from pupa.scrape import Scraper

from utils import lxmlize, CanadianLegislator as Legislator

import re

ASSEMBLY_PAGE = 'http://www.assnat.qc.ca/en/deputes/index.html'


class QuebecPersonScraper(Scraper):

  def get_people(self):
    page = lxmlize(ASSEMBLY_PAGE)
    for row in page.xpath('//*[@id="ListeDeputes"]/tbody/tr'):
      name_comma, division = [cell.xpath('string(.)') for cell in row[:2]]
      name = ' '.join(reversed(name_comma.strip().split(',')))
      email = row[3].xpath('string(.//a/@href)').replace('mailto:', '')
      detail_url = row[0][0].attrib['href']
      detail_page = lxmlize(detail_url)
      photo_url = detail_page.xpath('string(//img[@class="photoDepute"]/@src)')
      p = Legislator(name=name, post_id=division, role='MNA', image=photo_url)
      p.add_source(ASSEMBLY_PAGE)
      p.add_source(detail_url)
      p.add_contact('email', email, None)
      yield p

