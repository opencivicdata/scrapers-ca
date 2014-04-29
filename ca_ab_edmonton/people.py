from pupa.scrape import Scraper

from utils import lxmlize, CanadianLegislator as Legislator

import re

COUNCIL_PAGE = 'http://www.edmonton.ca/city_government/city_organization/city-councillors.aspx'
MAYOR_PAGE = 'http://www.edmonton.ca/city_government/city_organization/the-mayor.aspx'


class EdmontonPersonScraper(Scraper):

  def get_people(self):
    yield scrape_mayor()

    page = lxmlize(COUNCIL_PAGE)
    councillor_cells = page.xpath('//th[contains(text(), "Ward")]')
    for cell in councillor_cells:
      district = cell.text
      name = cell[1].text
      page_url = cell[1].attrib['href']
      page = lxmlize(page_url)

      p = Legislator(name=name, post_id=district, role='Councillor')
      p.add_source(COUNCIL_PAGE)
      p.add_source(page_url)

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
        elif 'Website' in contact_type or 'Facebook' in contact_type or 'Twitter' in contact_type:
          value = contact.xpath('./td/a/text()')[0]
          p.add_link(value, None)
        elif 'Telephone' in contact_type:
          p.add_contact('voice', value, 'legislature')
        elif 'Fax' in contact_type:
          p.add_contact('fax', value, 'legislature')
        elif 'Email' in contact_type:
          p.add_contact('email', value, None)
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
