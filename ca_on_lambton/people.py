from pupa.scrape import Scraper, Legislator

from utils import lxmlize, CONTACT_DETAIL_TYPE_MAP

import re

COUNCIL_PAGE = 'http://www.lambtononline.ca/home/government/accessingcountycouncil/countycouncillors/Pages/default.aspx'


class LambtonPersonScraper(Scraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)

    councillors = page.xpath('//div[@id="WebPartWPQ1"]/table/tbody/tr[1]')
    for councillor in councillors:
      name = councillor.xpath('.//td[1]//strong')
      name = name[0].text_content().strip().replace('Deputy ', '').replace('Warden ', '').replace('Mayor', '')
      role = councillor.xpath('.//td[1]//strong')[0].text_content().replace(name, '').strip()
      if not role:
        role = 'Councillor'
      if ',' in name:
        name = name.split(',')[0].strip()
      district = councillor.xpath('.//td[1]//p[contains(text(),",")]/text()')[0].split(',')[1].strip()

      p = Legislator(name=name, post_id=district, role=role)
      p.add_source(COUNCIL_PAGE)

      p.image = councillor.xpath('.//td[1]//img/@src')[0]

      info = councillor.xpath('.//td[2]')[0].text_content()
      residential_info = re.findall(r'(?<=Residence:)(.*)(?=Municipal Office:)', info, flags=re.DOTALL)[0]
      self.get_contacts(residential_info, 'residence', p)
      municipal_info = re.findall(r'(?<=Municipal Office:)(.*)', info, flags=re.DOTALL)[0]
      self.get_contacts(municipal_info, 'legislature', p)
      yield p

  def get_contacts(self, text, note, councillor):
    address = text.split('Telephone')[0]
    text = text.replace(address, '').split(':')
    for i, contact in enumerate(text):
      if i == 0:
        continue
      contact_type = next(x.strip() for x in re.findall(r'[A-Za-z ]+', text[i - 1]) if x.strip() and x.strip() != 'ext')
      if '@' in contact:
        contact = contact.strip()
      else:
        contact = re.findall(r'[0-9]{3}[- ][0-9]{3}-[0-9]{4}(?: ext\. [0-9]+)?', contact)[0].replace(' ', '-')

      if 'Fax' in contact_type:
        councillor.add_contact('fax', contact, note)
      elif 'Tel' in contact_type:
        councillor.add_contact('voice', contact, note)
      elif 'email' in contact_type:
        councillor.add_contact('email', contact, None)
      else:
        councillor.add_contact(CONTACT_DETAIL_TYPE_MAP[contact_type], contact, note)
