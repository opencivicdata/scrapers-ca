from pupa.scrape import Scraper, Legislator

from utils import lxmlize

import re

COUNCIL_PAGE = 'http://www.ville.quebec.qc.ca/apropos/vie_democratique/elus/conseil_municipal/membres.aspx'


class QuebecPersonScraper(Scraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)

    councillors = page.xpath('//div[contains(@class, "ligne")]')
    for councillor in councillors:

      name = ' '.join(councillor.xpath('.//h3')[0].text_content().strip().split(', ')[::-1])
      role = 'Councillor'
      if 'vacant' in name:
        continue
      district = councillor.xpath('./preceding-sibling::h2/text()')
      if district:
        district = district[-1]
      else:
        district = councillor.xpath('./parent::div/preceding-sibling::h2/text()')[-1]

      if 'Maire' in district:
        district = 'quebec'
        role = 'Mayor'

      p = Legislator(name=name, post_id=district, role=role)
      p.add_source(COUNCIL_PAGE)
      p.image = councillor.xpath('./p/img/@src')[0]

      phone = re.findall(r'T.l\. : ([0-9]{3} [0-9]{3}-[0-9]{4})(,.*([0-9]{4}))?', councillor.text_content())[0]
      if phone[-1]:
        phone = phone[0].replace(' ', '-') + ' x' + phone[-1]
      else:
        phone = phone[0].replace(' ', '-')
      p.add_contact('voice', phone, 'legislature')
      yield p
