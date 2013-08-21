from pupa.scrape import Scraper, Legislator

from utils import lxmlize

import re

COUNCIL_PAGE = 'http://www.town.lasalle.on.ca/Council/council-council.htm'


class LaSallePersonScraper(Scraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)
    councillors = page.xpath('//div[@align="center" and not(@class="background")]//td/p')
    for councillor in councillors:
      if not councillor.text_content().strip():
        continue
      name = councillor.xpath('./font/b/text()')
      if not name:
        name = councillor.xpath('./font/text()')
      if 'e-mail' in name[0]:
        name = councillor.xpath('./b/font/text()')
      name = name[0]

      p = Legislator(name=name, post_id="LaSalle")
      p.add_source(COUNCIL_PAGE)

      email = councillor.xpath('.//a[contains(@href, "mailto:")]/text()')[0]
      p.add_contact('email', email, None)

      phone = re.findall(r'(?<=phone:)(.*)(?=home)', councillor.text_content(), flags=re.DOTALL)
      if phone:
        p.add_contact('Phone', phone[0].strip(), None)

      home_phone = re.findall(r'(?<=home phone:)(.*)', councillor.text_content(), flags=re.DOTALL)[0]
      p.add_contact('Phone', home_phone.strip(), 'home')
      yield p
