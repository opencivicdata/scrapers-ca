from pupa.scrape import Scraper

from utils import lxmlize, CanadianLegislator as Legislator

import re

COUNCIL_PAGE = 'http://www.edmonton.ca/city_government/city_organization/city-councillors.aspx'
MAYOR_PAGE = 'http://www.edmonton.ca/city_government/city_organization/the-mayor.aspx'


class EdmontonPersonScraper(Scraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)

    yield scrape_mayor()
    councillors = page.xpath('//div[@id="contentArea"]//h3//a/@href')
    for councillor in councillors:
      page = lxmlize(councillor)
      district, name = page.xpath('//div[@id="contentArea"]/h1/text()')[0].split('-')

      p = Legislator(name=name, post_id=district, role='Councillor')
      p.add_source(COUNCIL_PAGE)
      p.add_source(councillor)

      image = page.xpath('//div[@id="contentArea"]//img/@src')
      if image:
        p.image = image[0]

      address = page.xpath('//address//p')
      if address:
        address = address[0].text_content()
        p.add_contact('address', address, 'legislature')

      contacts = page.xpath('//table[@class="contactListing"]//tr')
      for contact in contacts:
        contact_type = contact.xpath('./th/text()')[0]
        value = contact.xpath('./td//text()')[0]
        if 'Title' in contact_type:
          continue
        if 'Website' in contact_type or 'Facebook' in contact_type or 'Twitter' in contact_type:
          value = contact.xpath('./td/a/text()')[0]
          p.add_link(value, None)
        else:
          p.add_contact(contact_type, value, 'legislature')
      yield p


def scrape_mayor():
  page = lxmlize(MAYOR_PAGE)
  name = page.xpath('//strong[contains(text(), "Mayor")]/text()')[0].replace('Mayor', '').strip()

  p = Legislator(name=name, post_id='Edmonton', role='Mayor')
  p.add_source(MAYOR_PAGE)

  image = page.xpath('//div[@id="contentArea"]//img/@src')[0]
  p.image = image

  address = ' '.join(page.xpath('//address/p/text()'))
  phone = page.xpath('.//address/following-sibling::table/tbody/tr/td/text()')[0]
  fax = page.xpath('.//address/following-sibling::table/tbody/tr/td/text()')[1]

  p.add_contact('address', address, 'legislature')
  p.add_contact('voice', phone, 'legislature')
  p.add_contact('fax', fax, 'legislature')

  return p
