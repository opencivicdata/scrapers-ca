from pupa.scrape import Scraper, Legislator
from pupa.models import Person
from pupa.models import Organization

from utils import lxmlize

import re

COUNCIL_PAGE = 'http://www.edmonton.ca/city_government/city_organization/city-councillors.aspx'

class BurlingtonPersonScraper(Scraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)

    councillors = page.xpath('//div[@id="contentArea"]//h3//a/@href')
    for councillor in councillors:
      page = lxmlize(councillor)
      district, name = page.xpath('//div[@id="contentArea"]/h1/text()')[0].split('-')

      p = Legislator(name=name, post_id=district)
      p.add_source(COUNCIL_PAGE)
      p.add_source(councillor)

      address = page.xpath('//address//p')
      if address:
        address = address[0].text_content()
        p.add_contact('address', address, None)

      contacts = page.xpath('//table[@class="contactListing"]//tr')
      for contact in contacts:
        contact_type = contact.xpath('./th/text()')[0]
        contact = contact.xpath('./td//text()')[0]
        if 'Title' in contact_type:
          continue
        p.add_contact(contact_type, contact, None)
      print p._contact_details
      yield p
    