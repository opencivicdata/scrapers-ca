from pupa.scrape import Scraper, Legislator

from utils import lxmlize, CanadianScraper

import re

COUNCIL_PAGE = 'http://www.citywindsor.ca/mayorandcouncil/City-Councillors/Pages/City-Councillors.aspx'
MAYOR_PAGE = 'http://www.citywindsor.ca/mayorandcouncil/Pages/Biography-of-the-Mayor.aspx'


class WindsorPersonScraper(CanadianScraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)

    councillors = page.xpath('//div[@class="sectioning"]//p')[:-2]
    for councillor in councillors:
      name, district = councillor.xpath('./a/text()')[0].split(' - ')
      address = ''.join(councillor.xpath('./text()')[0:3])
      phone = councillor.xpath('./text()')[3].split(':')[1].strip().replace('(', '').replace(') ', '-')
      email = councillor.xpath('./a[contains(@href, "mailto")]/text()')[0]

      p = Legislator(name=name, post_id=district)
      p.add_source(COUNCIL_PAGE)
      p.role = 'Councillor'
      p.add_contact('address', address, 'legislature')
      p.add_contact('voice', phone, 'legislature')
      p.add_contact('email', email, None)
      p.image = councillor.xpath('./img/@src')[0]

      yield p

    page = lxmlize(MAYOR_PAGE)
    name = ' '.join(page.xpath('//p[contains(text(), "is married to")]/text()')[0].split()[:2])
    address = ' '.join(page.xpath('//p[contains(text(), "Mayor\'s Office")]/text()')[1:])
    phone, fax = page.xpath('//p[contains(text(), "Phone:")]/text()')[:-1]
    phone = phone.strip().replace('(', '').replace(') ', '-')
    fax = fax.strip().replace('(', '').replace(') ', '-')
    email = page.xpath('//a[contains(@href, "mailto:")]/text()')[0]

    p = Legislator(name=name, post_id='Windsor')
    p.add_source(MAYOR_PAGE)
    p.role = 'Mayor'
    p.add_contact('address', address, 'legislature')
    p.add_contact('voice', phone, 'legislature')
    p.add_contact('fax', fax, 'legislature')
    p.add_contact('email', email, None)
    p.image = page.xpath('//div[@class="sectioning"]//img[contains(@title, "Mayor")]/@src')[0]
    yield p
