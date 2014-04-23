# coding: utf-8
from pupa.scrape import Scraper

from utils import lxmlize, CanadianLegislator as Legislator

import re

COUNCIL_PAGE = 'http://www.assnat.qc.ca/fr/deputes/index.html'


class QuebecPersonScraper(Scraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)
    for row in page.xpath('//*[@id="ListeDeputes"]/tbody/tr'):
      name_comma, division = [cell.xpath('string(.)') for cell in row[:2]]
      name = ' '.join(reversed(name_comma.strip().split(',')))
      party = row[2].text_content()
      email = row[3].xpath('string(.//a/@href)').replace('mailto:', '')
      detail_url = row[0][0].attrib['href']
      detail_page = lxmlize(detail_url)
      photo_url = detail_page.xpath('string(//img[@class="photoDepute"]/@src)')
      division = division.replace(u'–', u'—')  # n-dash, m-dash
      p = Legislator(name=name, post_id=division, role='MNA', 
          party=party, image=photo_url)
      p.add_source(COUNCIL_PAGE)
      p.add_source(detail_url)
      if email:  # Premier may not have email.
        p.add_contact('email', email, None)
      yield p

