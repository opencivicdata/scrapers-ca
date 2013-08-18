from pupa.scrape import Scraper, Legislator

from utils import lxmlize

import re

COUNCIL_PAGE = 'http://www.ville.kirkland.qc.ca/portrait-municipal/conseil-municipal/elus-municipaux'

class KirklandPersonScraper(Scraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)

    councillors = page.xpath('//div[@id="PageContent"]/table/tbody/tr/td')
    for councillor in councillors:
      if not councillor.text_content().strip():
        continue
      if councillor == councillors[0]:
        district = 'kirkland'
      else:
        district = councillor.xpath('.//h2')[0].text_content()
      name = councillor.xpath('.//strong/text()')[0]

      phone = councillor.xpath('.//div[contains(text(), "#")]/text()')[0].replace('T ','').replace(' ','-').replace(',-#-',' x')
      email = councillor.xpath('.//a[contains(@href, "mailto:")]')[0].text_content()

      p = Legislator(name=name, post_id=district)
      p.add_source(COUNCIL_PAGE)
      p.add_contact('phone', phone, None)
      p.add_contact('email', email, None)
      yield p