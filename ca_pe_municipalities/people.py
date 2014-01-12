from pupa.scrape import Scraper, Legislator
from pupa.models import Organization
from utils import lxmlize

import re

COUNCIL_PAGE = 'http://www.gov.pe.ca/mapp/municipalitites.php'


class PrinceEdwardIslandMunicipalitiesPersonScraper(Scraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)

    districts = page.xpath('//div[@id="left-content" or @id="right-content"]//a')
    for district in districts:
      url = district.attrib['href']
      page = lxmlize(url)

      chamber = district.text_content() + ' Council'
      org = Organization(name=chamber, chamber=chamber, classification='legislature', jurisdiction_id=self.jurisdiction.jurisdiction_id)
      org.add_source(url)
      yield org

      info = page.xpath('//div[@style="WIDTH:750"]/dl')
      for contact in info:
        contact_type = contact.xpath('./dt')[0].text_content()
        contact = contact.xpath('./dd')[0].text_content().replace('(', '').replace(') ', '-')
        if 'Officials' in contact_type:
          break
        if 'Tel' in contact_type:
          phone = contact
        if 'Fac' in contact_type:
          fax = contact
        if 'Address' in contact_type:
          address = contact
        if 'Email' in contact_type:
          email = contact
        if 'Website' in contact_type:
          site = contact

      councillors = page.xpath('//div[@style="WIDTH:750"]/dl/dt[contains(text(), "Elected Officials")]/parent::dl/dd/pre/text()')[0].splitlines(True)
      for councillor in councillors:
        name = councillor.replace('(Mayor)', '').replace('(Deputy Mayor)', '').replace('(Chairperson)', '').strip()
        role = councillor.replace(name, '').strip()
        if not role:
          role = 'councillor'
        p = Legislator(name=name, post_id=district.text_content())
        p.add_source(COUNCIL_PAGE)
        p.add_source(url)
        p.add_membership(org, role=role, chamber=chamber)
        p.add_contact('voice', phone, None)
        p.add_contact('fax', fax, None)
        p.add_contact('address', address, None)
        p.add_contact('email', email, None)
        if site:
          p.add_link(site, None)
        yield p
