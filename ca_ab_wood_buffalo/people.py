from pupa.scrape import Scraper, Legislator

from utils import lxmlize, CanadianScraper

import re

COUNCIL_PAGE = 'http://www.woodbuffalo.ab.ca/Municipal-Government/Mayor-and-Council/Councillor-Profiles.htm'


class WoodBuffaloPersonScraper(CanadianScraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)
    organization = self.get_organization()
    yield organization

    mayor_url = page.xpath('//li[@id="pageid1075"]/div/a/@href')[0]
    yield scrape_mayor(mayor_url, organization)

    councillors = page.xpath('//table//a')
    for councillor in councillors:
      name = councillor.text_content().strip()
      if not name:
        continue
      district = councillor.xpath('./ancestor::table/preceding-sibling::h2/text()')[-1].split('-')[1]
      image = councillor.xpath('./parent::h3/preceding-sibling::a/img/@src')[0]

      url = councillor.attrib['href']
      page = lxmlize(url)

      p = Legislator(name=name, post_id=district)
      p.add_source(COUNCIL_PAGE)
      p.add_source(url)
      p.add_membership(organization, 'councillor')
      p.image = image

      contacts = page.xpath('//div[@id="content"]//div[@class="block"]/p/text()')
      for contact in contacts:
        if not re.search(r'[0-9]', contact):
          continue
        if not '(' in contact:
          contact_type = 'T'
        else:
          contact_type, contact = contact.split('(')
        contact = contact.replace(') ', '-').strip()
        if 'T' in contact_type:
          p.add_contact('voice', contact, 'office')
        if 'H' in contact_type:
          p.add_contact('voice', contact, 'Home')
        if 'C' in contact_type:
          p.add_contact('voice', contact, 'Cell')
        if 'F' in contact_type:
          p.add_contact('fax', contact, 'office')
      email = page.xpath('//div[@id="content"]//div[@class="block"]//a[contains(@href, "mailto:")]')[0].text_content()
      p.add_contact('email', email, None)
      yield p


def scrape_mayor(url, organization):
  page = lxmlize(url)
  name = page.xpath('//h1[@id="pagetitle"]/text()')[0].replace('Mayor', '').strip()
  image = page.xpath('//div[@id="content"]/p[1]/img/@src')[0]
  contact_url = page.xpath('//li[@id="pageid1954"]/a/@href')[0]
  page = lxmlize(contact_url)

  info = page.xpath('//div[@id="content"]/div[@class="block"][2]/p/text()')
  address = ' '.join(info[1:4])
  phone = info[4]
  fax = info[5]

  p = Legislator(name=name, post_id='wood buffalo')
  p.add_source(url)
  p.add_source(contact_url)
  p.add_membership(organization, role='mayor')
  p.add_contact('address', address, 'office')
  p.add_contact('voice', phone, 'office')
  p.add_contact('fax', fax, 'office')
  p.image = image
  return p
