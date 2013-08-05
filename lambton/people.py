from pupa.scrape import Scraper, Legislator
from larvae.person import Person
from larvae.organization import Organization

from .utils import lxmlize

import re

COUNCIL_PAGE = 'http://www.lambtononline.ca/home/government/accessingcountycouncil/countycouncillors/Pages/default.aspx'

class LambtonPersonScraper(Scraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)

    councillors = page.xpath('//div[@id="WebPartWPQ1"]/table/tbody/tr[1]')
    for councillor in councillors:
      name = councillor.xpath('.//td[1]//strong')
      name = name[0].text_content().strip().replace('Deputy ','').replace('Warden ','').replace('Mayor','')
      if ',' in name:
        name = name.split(',')[0].strip()
      district = councillor.xpath('.//td[1]//p[contains(text(),",")]/text()')[0].split(',')[1].strip()

      p = Legislator(name=name, district=district)
      p.add_source(COUNCIL_PAGE)

      info = councillor.xpath('.//td[2]')[0].text_content()
      residential_info = re.findall(r'(?<=Residence:)(.*)(?=Municipal Office:)', info, flags=re.DOTALL)[0]
      self.get_contacts(residential_info, 'Residence', p)
      municipal_info = re.findall(r'(?<=Municipal Office:)(.*)', info, flags=re.DOTALL)[0]
      self.get_contacts(municipal_info, 'Municipal Office', p)
      yield p

  def get_contacts(self, text, note, councillor):
    address = text.split('Telephone')[0]
    text = text.replace(address, '').split(':')
    for i, contact in enumerate(text):
      if i==0:
        continue
      contact_type = re.findall(r'[A-Za-z]+' ,text[i-1])[0]
      if '@' in contact:
        contact = contact.strip()
      else:
        contact = re.findall(r'[0-9]{3}[- ][0-9]{3}-[0-9]{4}', contact)[0].replace(' ','-')

      if 'Fax' in contact_type:
        councillor.add_contact('Fax', contact, note)
      elif 'Tel' in contact_type:
        councillor.add_contact('Phone', contact, note)
      elif 'email' in contact_type:
        councillor.add_contact('email', contact, note)
      else:
        councillor.add_contact('Phone', contact, note + ' ' + contact_type)


