# coding: utf-8
from pupa.scrape import Scraper

from utils import lxmlize, CanadianLegislator as Legislator

import re

COUNCIL_PAGE = 'http://www.ontla.on.ca/web/members/members_current.do'


class OntarioPersonScraper(Scraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)
    for row in page.xpath('//div[@id="currentMPPs"]/div[2]/div[2]/table//tr'):
      name_comma, riding = [cell.xpath('string(.)') for cell in row]
      name = ' '.join(name_comma.strip().split(',')[::-1])
      u_riding = riding.replace('--', u'\u2014')
      mpp_url = row[0][0].attrib['href']
      mpp_page = lxmlize(mpp_url)
      email = mpp_page.xpath('string(//div[@class="email"])')
      phone = mpp_page.xpath('string(//div[@class="phone"][1])')
      photo_url = mpp_page.xpath('string(//img[@class="mppimg"]/@src)')

      p = Legislator(name=name, post_id=u_riding, role='MPP', image=photo_url)
      p.add_source(COUNCIL_PAGE)
      p.add_source(mpp_url)
      p.add_contact('email', email, None)
      p.add_contact('voice', phone, 'legislature')
      yield p

