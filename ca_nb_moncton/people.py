# coding: utf-8
from pupa.scrape import Scraper

from utils import lxmlize, CanadianLegislator as Legislator

import re

COUNCIL_PAGE = 'http://www.moncton.ca/Government/City_Council.htm'


class MonctonPersonScraper(Scraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE, 'iso-8859-1')

    mayor_url = page.xpath('//li[@id="pageid193"]//a/@href')[0]
    yield scrape_mayor(mayor_url)

    councillors = page.xpath('//td[@class="cityfonts"]')
    for councillor in councillors:
      parts = [x.strip() for x in councillor.xpath('.//span/text()') if re.sub(u'\xa0', ' ', x).strip()]
      name = ' '.join(parts[:2])

      district = parts[2]
      if district == 'At Large':
        district = 'Moncton'
      elif district == 'Deputy Mayor':
        district = parts[3]

      url = councillor.xpath('.//a')[-1].attrib['href']
      page = lxmlize(url)

      p = Legislator(name=name, post_id=district, role='Councillor')
      p.add_source(COUNCIL_PAGE)
      p.add_source(url)
      p.image = councillor.xpath('.//img/@src')[0]

      email = page.xpath(
          'string(.//a[contains(@href, "mailto:")]/@href)')[len('mailto:'):]
      p.add_contact('email', email, None)

      contact_info = page.xpath('.//table[@class="whiteroundedbox"]//td/p[contains(text()," ")]')[0].text_content()
      phone_nos = re.findall(r'(([0-9]{3}-)?([0-9]{3}-[0-9]{4}))', contact_info)
      for phone_no in phone_nos:
        if len(re.sub(r'\D', '', phone_no[0])) == 7:
          phone = '506-%s' % phone_no[0]
        else:
          phone = phone_no[0]
        p.add_contact('voice', phone, 'legislature')
      yield p


def scrape_mayor(url):
  page = lxmlize(url)
  name = page.xpath('//meta[@name="description"]/@content')[0].split(',')[1]

  p = Legislator(name=name, post_id='Moncton', role='Mayor')
  p.add_source(url)

  p.image = page.xpath('//div[@id="content"]/p[1]/img/@src')[0]

  info = page.xpath('//table[@class="whiteroundedbox"]//tr[2]/td[1]')[1]
  address = ', '.join(info.xpath('./p[1]/text()')[1:4])
  address = re.sub(r'\s{2,}', ' ', address).strip()
  phone = info.xpath('.//p[2]/text()')[0].split(':')[1].strip()
  fax = info.xpath('.//p[2]/text()')[1].split(':')[1].strip()
  email = info.xpath('.//a/@href')[0].split(':')[1].strip()

  p.add_contact('address', address, 'legislature')
  if len(re.sub(r'\D', '', phone)) == 7:
    phone = '506-%s' % phone
  p.add_contact('voice', phone, 'legislature')
  p.add_contact('fax', fax, 'legislature')
  p.add_contact('email', email, None)

  return p
