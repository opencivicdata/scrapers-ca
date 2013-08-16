from pupa.scrape import Scraper, Legislator
from larvae.person import Person
from larvae.organization import Organization

from utils import lxmlize

import re

COUNCIL_PAGE = 'http://www.thunderbay.ca/City_Government/Your_Council.htm'

class ThunderBayPersonScraper(Scraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)

    councillors = page.xpath('//a[contains(@title, "Profile")][1]/@href')[:-1]
    for councillor in councillors:
      page = lxmlize(councillor)
      info = page.xpath('//table/tbody/tr/td[2]')[0]

      if len(info.xpath('./p[1]/strong')) > 1:
        name = info.xpath('./p/strong')[0].text_content()
        district = info.xpath('./p/strong')[1].text_content()
      else:
        name = info.xpath('./p/strong/em/strong//text()')
        district = 'Thunder Bay'
        if name:
          name = name[0]
          for text in name:
            if 'Ward' in text:
              district = text
        else:
          name = info.xpath('./p/strong/em/text()')[0]
      name = name.replace('Councillor', '').replace('Mayor', '').strip()

      p = Legislator(name=name, post_id=district)
      p.add_source(COUNCIL_PAGE)
      p.add_source(councillor)

      address = ', '.join(info.xpath('./p/text()')[0:2]).strip()
      address = re.sub(r'\s{2,}', ' ', address)

      p.add_contact('address', address, None)

      contacts = info.xpath('./p[2]/text()')
      for contact in contacts:
        contact_type, contact = contact.split(':')
        contact = contact.replace('(','').replace(') ','-').strip()
        if 'Fax' in contact_type:
          p.add_contact('Fax', contact, None)
        elif 'Email' in contact_type:
          break
        else:
          p.add_contact('Phone', contact, contact_type.strip())

      email = info.xpath('.//a[contains(@href, "mailto:")]')[0].text_content()
      p.add_contact('email', email, None)

      yield p


      # print name, district