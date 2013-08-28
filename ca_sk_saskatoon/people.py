from pupa.scrape import Scraper, Legislator

from utils import lxmlize, CanadianScraper

import re

COUNCIL_PAGE = "http://www.saskatoon.ca/CITY%20COUNCIL/YOUR%20WARD%20COUNCILLORS/Pages/default.aspx"


class SaskatoonPersonScraper(CanadianScraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)
    organization = self.get_organization()
    yield organization

    mayor_url = page.xpath('//td[@class="sask_LeftNavLinkContainer"]/a/@href')[0]
    yield scrape_mayor(mayor_url, organization)

    councillors = page.xpath('//td[@class="sask_LeftNavChildNodeContainer"]//a')
    for councillor in councillors:
      district, name = councillor.text_content().split(' - Councillor ')
      url = councillor.attrib['href']

      p = Legislator(name=name, post_id=district)
      p.add_source(COUNCIL_PAGE)
      p.add_source(url)
      p.add_membership(organization, role='councillor')

      page = lxmlize(url)
      contacts = page.xpath('//p[@class="para12"]')[0]
      if not contacts.text_content().strip():
        contacts = page.xpath('//p[@class="para12"]')[1]
      contacts = re.split(r'\xa0', contacts.text_content())
      contacts = [x for x in contacts if x.strip()]
      for i, contact in enumerate(contacts):
        if 'Contact' in contact:
          continue
        if contact == contacts[-1]:
          break
        contact_type = contact.replace(':', '').strip()
        value = contacts[i + 1].replace('(', '').replace(') ', '-').strip()
        if 'Fax' in contact_type:
          p.add_contact('Fax', value, 'office')
        if 'Phone' in contact_type:
          p.add_contact('Phone', value, contact_type.replace('Phone:', ''))
        if 'Email' in contact_type:
          p.add_contact('email', value, None)
      yield p


def scrape_mayor(url, organization):
  page = lxmlize(url)
  name = page.xpath('//tr/td/p')[-1]
  name = name.text_content().replace('Mayor', '')
  image = page.xpath('//div[@class="sask_ArticleBody"]//img/@src')[0]

  contact_url = page.xpath('//a[contains(text(), "Contact the Mayor")]/@href')[0]
  page = lxmlize(contact_url)

  address = ' '.join(page.xpath('//div[@id="ctl00_PlaceHolderMain_RichHtmlField1__ControlWrapper_RichHtmlField"]/p[4]/text()')[1:])
  phone = page.xpath('//div[@id="ctl00_PlaceHolderMain_RichHtmlField1__ControlWrapper_RichHtmlField"]/p[5]/span/text()')[0].replace('(', '').replace(') ', '-')
  fax = page.xpath('//div[@id="ctl00_PlaceHolderMain_RichHtmlField1__ControlWrapper_RichHtmlField"]/p[6]/span/text()')[0].replace('(', '').replace(') ', '-')

  p = Legislator(name=name, post_id='saskatoon')
  p.add_source(COUNCIL_PAGE)
  p.add_source(url)
  p.add_membership(organization, role='mayor')
  p.image = image
  p.add_contact('address', address, 'office')
  p.add_contact('phone', phone, 'office')
  p.add_contact('fax', fax, 'office')
  return p
