from pupa.scrape import Scraper, Legislator

from utils import lxmlize, CanadianScraper

import re

COUNCIL_PAGE = 'http://www.cotesaintluc.org/Administration'


class CoteSaintLucPersonScraper(CanadianScraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)
    organization = self.get_organization()
    yield organization

    mayor_url = page.xpath('//a[contains(text(), "Mayor")]/@href')[0]
    yield self.scrape_mayor(mayor_url, organization)

    councillors_url = page.xpath('//a[contains(text(), "Councillors")]/@href')[0]
    page = lxmlize(councillors_url)

    councillors = page.xpath('//div[@class="pane-content"]')[1:]
    for councillor in councillors:
      district = councillor.xpath('.//h3/text()')[0]
      name = councillor.xpath('.//p[contains(text(), "Councillor")]/strong/text()')[0]

      p = Legislator(name=name, post_id=district)
      p.add_source(COUNCIL_PAGE)
      p.add_source(councillors_url)
      p.add_membership(organization, role='councillor')

      p.image = councillor.xpath('.//img/@src')[0]

      phone = councillor.xpath('.//p[contains(text(), "Telephone")]/text()')[0].split(':')[1]
      p.add_contact('phone', phone, 'office')

      email = councillor.xpath('.//a[contains(@href, "mailto:")]')
      if email:
        email = email[0].text_content()
        p.add_contact('email', email, None)

      website = councillor.xpath('.//p[contains(text(), "Website")]/a')
      if website:
        website = website[0].attrib['href']
        p.add_link(website, 'personal site')

      yield p

  def scrape_mayor(self, url, organization):
    page = lxmlize(url)
    info = page.xpath('//div[@class="pane-content"]')[1]

    name = info.xpath('.//h3/text()')[0].replace('Mayor ', '')
    email = info.xpath('.//a[contains(@href, "mailto:")]/text()')[0]
    phone = info.xpath('.//p[contains(text(), "phone")]/text()')[0].replace('Telephone: ', '')

    p = Legislator(name=name, post_id='cote st-luc')
    p.add_source(COUNCIL_PAGE)
    p.add_membership(organization, role='mayor')
    p.image = info.xpath('.//img/@src')[0]
    p.add_source(url)
    p.add_contact('email', email, None)
    p.add_contact('phone', phone, 'office')
    return p
