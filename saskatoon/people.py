from pupa.scrape import Scraper, Legislator
from larvae.person import Person
from larvae.organization import Organization

from .utils import lxmlize

import re

COUNCIL_PAGE = "http://www.saskatoon.ca/CITY%20COUNCIL/YOUR%20WARD%20COUNCILLORS/Pages/default.aspx"

class SaskatoonPersonScraper(Scraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)

    councillors = page.xpath('//td[@class="sask_LeftNavChildNodeContainer"]//a')
    for councillor in councillors:
      district, name = councillor.text_content().split(' - Councillor ')
      url = councillor.attrib['href']

      p = Legislator(name=name, district=district)
      p.add_source(COUNCIL_PAGE)
      p.add_source(url)

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
        value = contacts[i+1].replace('(','').replace(') ', '-').strip()
        if 'Fax' in contact_type:
          p.add_contact('Fax', value, None)
        if 'Phone' in contact_type:
          p.add_contact('Phone', value, contact_type.replace('Phone:', ''))
        if 'Email' in contact_type:
          p.add_contact('email', value, None)
      yield p
