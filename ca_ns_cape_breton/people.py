from pupa.scrape import Scraper, Legislator

from utils import lxmlize, CanadianScraper

import re

COUNCIL_PAGE = 'http://www.cbrm.ns.ca/councillors.html'


class CapeBretonPersonScraper(CanadianScraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)
    organization = self.get_organization()
    yield organization

    councillors = page.xpath('//table[@class="table_style"]/tbody/tr')[1:]
    for councillor in councillors:
      name = councillor.xpath('.//a')[0].text_content()
      district = councillor.xpath('.//strong')[0].text_content()

      address = councillor.xpath('.//td')[3].text_content().replace("\r\n", ', ')
      phone = councillor.xpath('.//td[5]/p/text()')[0].split(':')[1].replace("(", '').replace(") ", '-')
      fax = councillor.xpath('.//td[5]/p/text()')[1].split(':')[1].replace("(", '').replace(") ", '-')

      p = Legislator(name=name, post_id=district)
      p.add_source(COUNCIL_PAGE)
      p.add_membership(organization, role='councillor')
      p.add_contact('address', address, 'office')
      p.add_contact('phone', phone, 'office')
      p.add_contact('fax', fax, 'office')

      councillor_url = councillor.xpath('.//a/@href')[0]
      p.add_source(councillor_url)
      page = lxmlize(councillor_url)
      p.image = page.xpath('//img[@class="image_left"]/@src')[0]
      yield p
