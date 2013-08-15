from pupa.scrape import Scraper, Legislator
from larvae.person import Person
from larvae.organization import Organization

from utils import lxmlize

import re

COUNCIL_PAGE = 'http://city.summerside.pe.ca/mayor-and-council/pages/2012/2/councillors/'
MAYOR_PAGE = 'http://city.summerside.pe.ca/mayor-and-council/pages/2012/2/mayor/'

class SummersidePersonScraper(Scraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)

    yield self.scrape_mayor()

    councillors = page.xpath('//div[@class="articlebody-inside"]//p[contains(text(),"-")]')
    for councillor in councillors:
      url = councillor.xpath('.//a')[0].attrib['href'].replace('../','')
      page = lxmlize(url)

      name = page.xpath('//div[@class="articletitle"]/h1')[0].text_content().replace('Councillor', '').replace('Deputy Mayor', '')
      district = page.xpath('//div[@class="articlebody-inside"]/p')[0].text_content()

      p = Legislator(name=name, post_id=district)
      p.add_source(COUNCIL_PAGE)
      p.add_source(url)

      contacts = page.xpath('//div[@class="articlebody-inside"]/p')[1].text_content().replace('Biography','').replace('Committees','').split(':')
      for i, contact in enumerate(contacts):
        if i==0 or not contact:
          continue
        contact_type = re.findall(r'([A-Z][a-z]+)', contacts[i-1])[0]
        if contact_type != 'Address':
          contact = re.split(r'[A-Z]', contact)[0]
        p.add_contact(contact_type.lower(), contact, None)
      yield p

  def scrape_mayor(self):
    page = lxmlize(MAYOR_PAGE)

    name = page.xpath('//div[@class="articletitle"]/h1')[0].text_content().replace('Mayor','')

    p = Legislator(name=name, post_id='summerside')
    p.add_source(MAYOR_PAGE)

    info = page.xpath('//div[@class="articlebody-inside"]/p')
    phone = re.findall(r'to (.*)', info[1].text_content())[0]
    address = info[3].text_content().replace('by mail: ', '') +' '+ info[4].text_content()
    email = info[5].xpath('.//a[contains(@href, "mailto:")]')[0].text_content()

    p.add_contact('phone', phone, None)
    p.add_contact('address', address, None)
    p.add_contact('email', email, None)

    return p