from pupa.scrape import Scraper, Legislator

from utils import lxmlize, CanadianScraper, CONTACT_DETAIL_TYPE_MAP

import re

COUNCIL_PAGE = 'http://www.chatham-kent.ca/Council/councilmembers/Pages/CouncilMembers.aspx'


class ChathamKentPersonScraper(CanadianScraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)
    organization = self.get_organization()
    yield organization

    wards = page.xpath('//table[@class="ms-rteTable-4"]')
    for ward in wards:
      district = ward.xpath('.//p')[0].text_content()
      if 'Mayor' in district:
        district = 'chatham-kent'
        role = 'mayor'
      else:
        district = re.findall(r'(?<=Council )(.*)(?=\()', district)[0]
        role = 'councillor'

      councillors = ward.xpath('.//a')
      for councillor in councillors:
        name = councillor.text_content()
        url = councillor.attrib['href']
        page = lxmlize(url)

        p = Legislator(name=name, post_id=district)
        p.add_source(COUNCIL_PAGE)
        p.add_source(url)
        p.add_membership(organization, role=role)

        p.image = page.xpath('//div[@class="pageContent"]//img/@src')[0]

        address = page.xpath('//div[@class="div_contact_us_content_address"]')[0].text_content()
        p.add_contact('address', address, 'legislature')

        contacts = page.xpath('//div[@class="div_contact_us_content_kv"]/div')
        for contact in contacts:
          contact_type, contact = contact.text_content().split(':')
          contact_type = CONTACT_DETAIL_TYPE_MAP[contact_type.strip()]
          p.add_contact(contact_type, contact.strip(), None if contact_type == 'email' else 'legislature')
        yield p
