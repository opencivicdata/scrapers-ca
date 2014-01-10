from pupa.scrape import Scraper, Legislator

from utils import lxmlize, CanadianScraper

import re

COUNCIL_PAGE = 'http://www.ville.brossard.qc.ca/Ma-ville/conseil-municipal.aspx?lang=en-CA'


class BrossardPersonScraper(CanadianScraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)
    organization = self.get_organization()
    yield organization

    councillors = page.xpath('//a[contains(@href, "mailto:")]')[1:]
    info = councillors[1].xpath('.//parent::div/text()')
    for num, councillor in enumerate(councillors):
      name = councillor.text_content()
      email = councillor.attrib['href'].split(':')[1].split('?')[0]
      district = re.sub(r'(?<=[0-9]) (.) (?=S)', ', ', info.pop(0))
      role = 'councillor'
      if 'Mayor' in district:
        district = 'brossard'
        role = 'mayor'
      phone = info.pop(0).replace('ext. ', 'x').strip()

      p = Legislator(name=name, post_id=district)
      p.add_source(COUNCIL_PAGE)
      p.add_membership(organization, role=role)

      image = page.xpath('//div[@class="slide_wrap"]//a[contains(@style, "background-image:url") and contains(@style, "%s")]/@style' % name.split()[0])[0]
      p.image = re.findall(r'\((.*)\)', image)[0]

      p.add_contact('email', email, None)
      p.add_contact('voice', phone, 'office')
      yield p
