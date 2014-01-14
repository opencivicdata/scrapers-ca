from pupa.scrape import Scraper, Legislator

from utils import lxmlize, CONTACT_DETAIL_NOTE_MAP

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
        role = 'Councillor'
      elif 'At Large' in info.text_content():
        name = info.xpath('./p/strong')[0].text_content()
        district = 'Thunder Bay'
        role = 'Councillor'
      else:
        name = info.xpath('./p/strong')[0].text_content()
        district = 'Thunder Bay'
        role = 'Mayor'
      name = name.replace('Councillor', '').replace('At Large', '').replace('Mayor', '').strip()

      p = Legislator(name=name, post_id=district, role=role)
      p.add_source(COUNCIL_PAGE)
      p.add_source(councillor)

      p.image = page.xpath('//td[@valign="top"]/img/@src')[0]

      address = ', '.join(info.xpath('./p/text()')[0:2]).strip()
      address = re.sub(r'\s{2,}', ' ', address)

      p.add_contact('address', address, 'legislature')

      contacts = info.xpath('./p[2]/text()')
      for contact in contacts:
        contact_type, contact = contact.split(':')
        contact = contact.replace('(', '').replace(') ', '-').strip()
        if 'Fax' in contact_type:
          p.add_contact('fax', contact, 'legislature')
        elif 'Email' in contact_type:
          break
        else:
          p.add_contact('voice', contact, CONTACT_DETAIL_NOTE_MAP[contact_type.strip()])

      email = info.xpath('.//a[contains(@href, "mailto:")]')[0].text_content()
      p.add_contact('email', email, None)

      yield p
