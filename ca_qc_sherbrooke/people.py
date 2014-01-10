from pupa.scrape import Scraper, Legislator

from utils import lxmlize, CanadianScraper

import re

COUNCIL_PAGE = 'http://www.ville.sherbrooke.qc.ca/mairie-et-vie-democratique/conseil-municipal/elus-municipaux/'


class SherbrookePersonScraper(CanadianScraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)
    organization = self.get_organization()
    yield organization

    councillors = page.xpath('//div[@id="c2087"]//a')
    for councillor in councillors:
      name = councillor.text_content()
      url = councillor.attrib['href']
      page = lxmlize(url)
      district = page.xpath('//h2/text()')[0]
      role = 'councillor'
      if 'Maire' in district:
        district = 'Sherbrooke'
        role = 'mayor'
      p = Legislator(name=name, post_id=district)
      p.add_source(COUNCIL_PAGE)
      p.add_source(url)
      p.add_membership(organization, role=role)
      p.image = page.xpath('//div[@id="conseiller-photo"]//img/@src')[0]
      phone = page.xpath('//li[contains(text(), "phone")]/text()')[0].split(':')[1].strip().replace(' ', '-')
      p.add_contact('voice', phone, None)
      email = page.xpath('//a[contains(@href, "mailto:")]/@href')
      if email:
        email = email[0].split(':')[1]
        p.add_contact('email', email, None)
      yield p
