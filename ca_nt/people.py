# coding: utf-8
from pupa.scrape import Scraper

from utils import lxmlize, CanadianLegislator as Legislator

import re

COUNCIL_PAGE = 'http://www.assembly.gov.nt.ca/meet-members'


class NorthwestTerritoriesPersonScraper(Scraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)

    member_cells = page.xpath(
        '//div[@class="views-field views-field-field-picture"]/'
        'parent::td')
    for cell in member_cells:
      name = cell[1].text_content().replace(' .', '. ') # typo on page
      riding = cell[2].text_content()
      if 'Mackenzie Delta' in riding:
        riding = 'Mackenzie-Delta'
      detail_url = cell[0].xpath('string(.//a/@href)')
      detail_page = lxmlize(detail_url)
      photo_url = detail_page.xpath(
          'string(//div[@class="field-item even"]/img/@src)')
      email = detail_page.xpath('string(//a[contains(@href, "mailto:")])')

      contact_text = detail_page.xpath(
          'string(//div[@property="content:encoded"]/p[1])')
      phone = re.search(r'P(hone)?: ([-0-9]+)', contact_text).group(2)

      p = Legislator(name=name, post_id=riding, role='MLA', image=photo_url)
      p.add_source(COUNCIL_PAGE)
      p.add_source(detail_url)
      p.add_contact('email', email, None)
      p.add_contact('voice', phone, 'legislature')
      yield p
