# coding: utf-8
from __future__ import unicode_literals

from pupa.scrape import Scraper

from utils import lxmlize, CanadianLegislator as Legislator

import re
from six.moves.urllib.parse import urljoin
from itertools import takewhile

COUNCIL_PAGE = 'http://www.regionofwaterloo.ca/en/regionalgovernment/regionalcouncil.asp'
CHAIR_URL = 'http://www.regionofwaterloo.ca/en/regionalGovernment/regionalchairandsupportstaff.asp'


class WaterlooPersonScraper(Scraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)

    regions = page.xpath('//*[@id="contentIntleft"]//h3')[1:]
    for region in regions:
      # the links in all <p> tags immediately following each <h3>
      councillors = [elem[0] for elem in
                     takewhile(lambda elem: elem.tag == 'p',
                               region.xpath('./following-sibling::*'))]
      for councillor in councillors:
        post = re.search('of (.*)', region.text).group(1)
        p = Legislator(name=councillor.text, post_id=post, role='Councillor')
        p.add_source(COUNCIL_PAGE)
        councillor_url = councillor.attrib['href']
        p.add_source(councillor_url)
        email, phone, address, photo_url = councillor_data(councillor_url)
        p.add_contact('email', email, None)
        p.add_contact('voice', phone, 'legislature')
        p.add_contact('address', address, 'legislature')
        p.image = photo_url
        yield p

    chairpage = lxmlize(CHAIR_URL)
    name = re.search('Chair (.*) -',
                     chairpage.xpath('string(//title)')).group(1)
    email = chairpage.xpath('string(//a[contains(text(), "E-mail")]/@href)')
    phone = chairpage.xpath('string((//span[@class="labelTag"][contains(text(), "Phone")]/parent::*/text())[1])').strip(':')
    address = '\n'.join(
        chairpage.xpath('//div[@class="contactBody"]//p[1]/text()'))
    photo_url_src = chairpage.xpath(
        'string(//div[@id="contentIntleft"]//img[1]/@src)')
    photo_url = urljoin(CHAIR_URL, photo_url_src)
    p = Legislator(name=name, post_id='Waterloo', role='Regional Chair')
    p.add_source(CHAIR_URL)
    p.add_contact('email', email, None)
    p.add_contact('voice', phone, 'legislature')
    p.add_contact('address', address, 'legislature')
    p.image = photo_url
    yield p


def councillor_data(url):
  page = lxmlize(url)
  email = page.xpath('string(//a[contains(text(), "Email Councillor")]/@href)')
  phone = page.xpath('string((//span[@class="labelTag"][contains(text(), "Phone")]/parent::*/text())[1])').strip(':')
  address = '\n'.join(page.xpath('//div[@class="contactBody"]//p[1]/text()'))
  photo_url_src = page.xpath('string(//div[@id="contentIntleft"]//img[1]/@src)')
  photo_url = urljoin(url, photo_url_src)
  return email, phone, address, photo_url
