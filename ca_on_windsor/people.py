from pupa.scrape import Scraper

from utils import lxmlize, CanadianLegislator as Legislator

import re
from urlparse import urljoin

COUNCIL_PAGE = 'http://www.citywindsor.ca/mayorandcouncil/City-Councillors/Pages/City-Councillors.aspx'
MAYOR_PAGE = 'http://www.citywindsor.ca/mayorandcouncil/Pages/Biography-of-the-Mayor.aspx'


class WindsorPersonScraper(Scraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)

    councillor_links = page.xpath(
        '//span[@class="textimagetype"]//a[contains(text(), "- Ward")]')
    for councillor_link in councillor_links:
      name, district = councillor_link.text.split(' - ')
      cpage_url = councillor_link.attrib['href']
      cpage = lxmlize(cpage_url)
      p = Legislator(name=name, post_id=district, role='Councillor')
      p.add_source(COUNCIL_PAGE)
      p.add_source(cpage_url)

      email = cpage.xpath('string(//a[contains(@href, "@")])')
      p.add_contact('email', email, None)

      phone = cpage.xpath(
          'string(//text()[contains(., "Phone")])').split(':')[1]
      p.add_contact('voice', phone, 'legislature')

      img_url_rel = cpage.xpath(
          'string(//span[@class="textimagetype"]/img/@src)')
      img_url = urljoin(cpage_url, img_url_rel)
      p.image = img_url

      yield p

    page = lxmlize(MAYOR_PAGE)
    name = ' '.join(page.xpath('//p[contains(text(), "is married to")]/text()')[0].split()[:2])
    address = ' '.join(page.xpath('//p[contains(text(), "Mayor\'s Office")]/text()')[1:])
    phone, fax = page.xpath('//p[contains(text(), "Phone:")]/text()')[:-1]
    phone = phone.strip().replace('(', '').replace(') ', '-')
    fax = fax.strip().replace('(', '').replace(') ', '-').split(':')[1]
    email = page.xpath('//a[contains(@href, "mailto:")]/text()')[0]

    p = Legislator(name=name, post_id='Windsor', role='Mayor')
    p.add_source(MAYOR_PAGE)
    p.add_contact('address', address, 'legislature')
    p.add_contact('voice', phone, 'legislature')
    p.add_contact('fax', fax, 'legislature')
    p.add_contact('email', email, None)
    p.image = page.xpath('//div[@class="sectioning"]//img[contains(@title, "Mayor")]/@src')[0]
    yield p
