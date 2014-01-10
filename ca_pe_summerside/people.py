from pupa.scrape import Scraper, Legislator

from utils import lxmlize, CanadianScraper

import re

COUNCIL_PAGE = 'http://city.summerside.pe.ca/mayor-and-council/pages/2012/2/councillors/'
MAYOR_PAGE = 'http://city.summerside.pe.ca/mayor-and-council/pages/2012/2/mayor/'
CONTACT_DETAIL_TYPE_MAP = {
  'Address': 'address',
  'Email': 'email',
  'Fax': 'fax',
  'Phone': 'voice',
}


class SummersidePersonScraper(CanadianScraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)
    organization = self.get_organization()
    yield organization

    yield self.scrape_mayor(organization)

    councillors = page.xpath('//div[@class="articlebody-inside"]//p[contains(text(),"-")]')
    for councillor in councillors:
      url = councillor.xpath('.//a')[0].attrib['href'].replace('../', '')
      page = lxmlize(url)

      name = page.xpath('//div[@class="articletitle"]/h1')[0].text_content().replace('Councillor', '').replace('Deputy Mayor', '')
      district = page.xpath('//div[@class="articlebody-inside"]/p')[0].text_content()

      p = Legislator(name=name, post_id=district)
      p.add_source(COUNCIL_PAGE)
      p.add_source(url)
      p.add_membership(organization, role='councillor')

      p.image = page.xpath('//div[@class="articlebody-inside"]/p/img/@src')[0]

      contacts = page.xpath('//div[@class="articlebody-inside"]/p')[1].text_content().replace('Biography', '').replace('Committees', '').split(':')
      for i, contact in enumerate(contacts):
        if i == 0 or not contact:
          continue
        contact_type = re.findall(r'([A-Z][a-z]+)', contacts[i - 1])[0]
        if contact_type != 'Address':
          contact = re.split(r'[A-Z]', contact)[0]
        p.add_contact(CONTACT_DETAIL_TYPE_MAP[contact_type], contact, 'legislature')
      yield p

  def scrape_mayor(self, organization):
    page = lxmlize(MAYOR_PAGE)

    name = page.xpath('//div[@class="articletitle"]/h1')[0].text_content().replace('Mayor', '')

    p = Legislator(name=name, post_id='summerside')
    p.add_source(MAYOR_PAGE)
    p.add_membership(organization, role='mayor')
    p.image = page.xpath('//div[@class="articlebody-inside"]/p/img/@src')[0]

    info = page.xpath('//div[@class="articlebody-inside"]/p')
    phone = re.findall(r'to (.*)', info[1].text_content())[0]
    address = info[3].text_content().replace('by mail: ', '') + ' ' + info[4].text_content()
    email = info[5].xpath('.//a[contains(@href, "mailto:")]')[0].text_content()

    p.add_contact('voice', phone, 'legislature')
    p.add_contact('address', address, 'legislature')
    p.add_contact('email', email, None)

    return p
