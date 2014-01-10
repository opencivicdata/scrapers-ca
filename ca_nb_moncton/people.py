from pupa.scrape import Scraper, Legislator

from utils import lxmlize, CanadianScraper

import re

COUNCIL_PAGE = 'http://www.moncton.ca/Government/City_Council.htm'


class MonctonPersonScraper(CanadianScraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)
    organization = self.get_organization()
    yield organization

    mayor_url = page.xpath('//li[@id="pageid193"]//a/@href')[0]
    yield scrape_mayor(mayor_url, organization)

    councillors = page.xpath('//td[@class="cityfonts"]')
    for councillor in councillors:
      name = councillor.xpath('.//a')[0].text_content()
      district = councillor.xpath('.//span/text()')[1]

      email = councillor.xpath('.//a')[0].attrib['href'].replace('mailto:', '')

      url = councillor.xpath('.//a')[-1].attrib['href']
      page = lxmlize(url)

      p = Legislator(name=name, post_id=district)
      p.add_source(COUNCIL_PAGE)
      p.add_source(url)
      p.add_membership(organization, role='councillor')
      p.add_contact('email', email, None)
      p.image = councillor.xpath('.//img/@src')[0]

      contact_info = page.xpath('.//table[@class="whiteroundedbox"]//td/p[contains(text()," ")]')[0].text_content()
      phone_nos = re.findall(r'(([0-9]{3}-)?([0-9]{3}-[0-9]{4}))', contact_info)
      for phone in phone_nos:
        p.add_contact('voice', phone[0], 'legislature')
      yield p


def scrape_mayor(url, organization):
  page = lxmlize(url)
  name = ' '.join(page.xpath('//div[@id="content"]/p[2]/text()')[0].split()[1:3])

  p = Legislator(name=name, post_id='moncton')
  p.add_source(url)
  p.add_membership(organization, role='mayor')

  p.image = page.xpath('//div[@id="content"]/p[1]/img/@src')[0]

  info = page.xpath('//table[@class="whiteroundedbox"]//tr[2]/td[1]')[1]
  address = ', '.join(info.xpath('./p[1]/text()')[1:4])
  address = re.sub(r'\s{2,}', ' ', address).strip()
  phone = info.xpath('.//p[2]/text()')[0].split(':')[1].strip()
  fax = info.xpath('.//p[2]/text()')[1].split(':')[1].strip()
  email = info.xpath('.//a/@href')[0].split(':')[1].strip()

  p.add_contact('address', address, 'legislature')
  p.add_contact('voice', phone, 'legislature')
  p.add_contact('fax', fax, 'legislature')
  p.add_contact('email', email, None)

  return p
