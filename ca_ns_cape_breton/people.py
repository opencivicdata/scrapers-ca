from __future__ import unicode_literals
from pupa.scrape import Scraper

import re

from six.moves.urllib.parse import urljoin

from utils import CanadianScraper, CanadianPerson as Person

COUNCIL_PAGE = 'http://www.cbrm.ns.ca/councillors.html'
MAYOR_PAGE = 'http://www.cbrm.ns.ca/mayor.html'


class CapeBretonPersonScraper(CanadianScraper):

  def scrape(self):
    page = self.lxmlize(COUNCIL_PAGE)

    councillors = page.xpath('//table[@class="table_style"]/tbody/tr')[1:]
    for councillor in councillors:
      name = councillor.xpath('.//a')[0].text_content()
      district = 'District %s' % councillor.xpath('.//strong')[0].text_content()

      address = councillor.xpath('.//td')[3].text_content().replace("\r\n", ', ')
      phone = councillor.xpath('.//td[5]/p/text()')[0].split(':')[1].replace("(", '').replace(") ", '-')
      fax = councillor.xpath('.//td[5]/p/text()')[1].split(':')[1].replace("(", '').replace(") ", '-')

      p = Person(primary_org='legislature', name=name, district=district, role='Councillor')
      p.add_source(COUNCIL_PAGE)
      p.add_contact('address', address, 'legislature')
      p.add_contact('voice', phone, 'legislature')
      p.add_contact('fax', fax, 'legislature')

      councillor_url = councillor.xpath('.//a/@href')[0]
      p.add_source(councillor_url)
      page = self.lxmlize(councillor_url)
      p.image = page.xpath('//img[@class="image_left"]/@src')[0]
      yield p

    mayorpage = self.lxmlize(MAYOR_PAGE)
    name_elem = mayorpage.xpath('//strong[contains(text(), "About")]')[0]
    name = re.search('About Mayor (.+):', name_elem.text).group(1)
    photo_url = mayorpage.xpath('string(//span/img/@src)')
    address_and_tel_elem = mayorpage.xpath(
      '//strong[contains(text(), "Contact")]/ancestor::p/'
      'following-sibling::p[1]')[0]
    address = address_and_tel_elem[0].text_content()
    phone = address_and_tel_elem[2].text.split(':')[1]

    p = Person(primary_org='legislature', name=name, district='Cape Breton', role='Mayor')
    p.add_source(MAYOR_PAGE)
    p.add_contact('address', address, 'legislature')
    p.add_contact('voice', phone, 'legislature')
    # email is protected through JS
    p.image = photo_url
    yield p
