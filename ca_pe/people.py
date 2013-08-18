from pupa.scrape import Scraper, Legislator

from utils import lxmlize

import re

COUNCIL_PAGE = 'http://www.gov.pe.ca/mapp/municipalitites.php'

class PrinceEdwardIslandPersonScraper(Scraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)

    districts = page.xpath('//div[@id="left-content" or @id="right-content"]//a')
    for district in districts:
      url = district.attrib['href']
      page = lxmlize(url)


      info = page.xpath('//div[@style="WIDTH:750"]/dl')
      for contact in info:
        contact_type = contact.xpath('./dt')[0].text_content()
        contact = contact.xpath('./dd')[0].text_content().replace('(','').replace(') ','-')
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
        name = councillor.replace('(Mayor)','').replace('(Deputy Mayor)','').replace('(Chairperson)','').strip()
        p = Legislator(name=name, post_id=district.text_content())
        p.add_source(COUNCIL_PAGE)
        p.add_source(url)
        p.add_contact('Phone', phone, None)
        p.add_contact('Fax', fax, None)
        p.add_contact('address', address, None)
        p.add_contact('email', email, None)
        if site:
          p.add_link(site, 'website')
        yield p
