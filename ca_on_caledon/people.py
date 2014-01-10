from pupa.scrape import Scraper, Legislator

from utils import lxmlize, CanadianScraper

import re

COUNCIL_PAGE = 'http://www.town.caledon.on.ca/en/townhall/council.asp'


class CaledonPersonScraper(CanadianScraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)
    organization = self.get_organization()
    yield organization

    mayor_url = page.xpath('//div[@id="printAreaContent"]/ul/li/strong/a/@href')[0]
    yield scrape_mayor(mayor_url, organization)

    councillors = page.xpath('//div[@id="printAreaContent"]//table//td')[2:]
    for councillor in councillors:
      district, name = councillor.text_content().split('-')
      url = councillor.xpath('.//a')[0].attrib['href']

      p = Legislator(name=name, post_id=district)
      p.add_source(COUNCIL_PAGE)
      p.add_source(url)
      p.add_membership(organization, role='councillor')

      page = lxmlize(url)

      info = page.xpath('//table[@summary="Councillor"]/tbody/tr/td[2]')[0]
      info = info.text_content().strip().splitlines(True)
      info = [x for x in info if not x == u'\xa0\n']
      address = info[1]
      email = re.findall(r'[a-z]+.[a-z]+@caledon.ca', info[2])[0]
      numbers = re.findall(r'[0-9]{3}.[0-9]{3}. ?[0-9]{4}', info[2])
      phone = numbers[0]
      fax = numbers[1]

      p.image = page.xpath('//table[@summary="Councillor"]//img/@src')[0]

      p.add_contact('address', address, 'office')
      p.add_contact('email', email, None)
      p.add_contact('voice', phone, 'office')
      p.add_contact('fax', fax, 'office')

      yield p


def scrape_mayor(url, organization):
  page = lxmlize(url)

  name = page.xpath('//div[@id="printAreaContent"]/h1/strong/text()')[0].replace('Mayor', '').strip()
  address = page.xpath('//strong[contains(text(), "mail")]/parent::p/text()')[1].replace(':', '').strip()
  phone = page.xpath('//strong[contains(text(), "phone")]/parent::p/text()')[1].split()[1]

  p = Legislator(name=name, post_id='caledon')
  p.add_source(COUNCIL_PAGE)
  p.add_source(url)
  p.add_membership(organization, role='mayor')
  p.image = page.xpath('//h2[contains(text(), "About me")]/img/@src')[0]
  p.add_contact('address', address, 'office')
  p.add_contact('voice', phone, 'office')
  return p
