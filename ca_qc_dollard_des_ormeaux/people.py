from pupa.scrape import Scraper, Legislator

from utils import lxmlize

import re

COUNCIL_PAGE = 'http://www.ville.ddo.qc.ca/en/default.asp?contentID=17'


class DollardDesOrmeauxPersonScraper(Scraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)

    general_contacts = page.xpath('//p[@class="large_title"]/following-sibling::p/text()')
    general_phone = general_contacts[0]
    general_fax = general_contacts[1]
    general_email = page.xpath('//p[@class="large_title"]/following-sibling::p//a[contains(@href, "mailto:")]')[0].text_content()

    councillors = page.xpath('//tr/td/p/strong')
    for councillor in councillors:

      if 'Mayor' in councillor.text_content():
        name = councillor.text_content().replace('Mayor', '')
        district = 'dollard-des-ormeaux'
        role = 'Mayor'
      else:
        name = re.split(r'[0-9]', councillor.text_content())[1]
        district = 'District ' + re.findall(r'[0-9]', councillor.text_content())[0]
        role = 'Councillor'

      p = Legislator(name=name, post_id=district)
      p.add_source(COUNCIL_PAGE)
      p.role = role
      p.image = councillor.xpath('./parent::p/parent::td/parent::tr/preceding-sibling::tr//img/@src')[0]

      email = councillor.xpath('./parent::p/following-sibling::p//a[contains(@href, "mailto:")]')
      if email:
        p.add_contact('email', email[0].text_content(), None)

      p.add_contact('voice', general_phone, 'legislature')
      p.add_contact('fax', general_fax, 'legislature')
      p.add_contact('email', general_email, None)

      yield p
