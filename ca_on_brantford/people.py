from pupa.scrape import Scraper, Legislator

from utils import lxmlize, CanadianScraper

import re

COUNCIL_PAGE = 'http://www.brantford.ca/govt/council/members/Pages/default.aspx'


class BrantfordPersonScraper(CanadianScraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)
    organization = self.get_organization()
    yield organization

    yield scrape_mayor(organization)

    councillors = page.xpath('//div[@id="centre_content"]//tr')
    for councillor in councillors:
      if 'Position' in councillor.text_content():
        continue

      district = councillor.xpath('./td')[0].text_content().replace('Councillor', '')
      name = councillor.xpath('./td')[1].text_content()
      url = councillor.xpath('./td/a')[0].attrib['href']

      p = Legislator(name=name, post_id=district)
      p.add_source(COUNCIL_PAGE)
      p.add_source(url)
      p.add_membership(organization, role='councillor')

      page = lxmlize(url)

      address = page.xpath('//div[@id="centre_content"]//p')[0].text_content().replace("\r\n", ', ')
      email = page.xpath('//a[contains(@href,"mailto:")]')[0].attrib['href'].replace('mailto:', '')
      p.add_contact('address', address, None)
      p.add_contact('email', email, None)

      p.image = page.xpath('//div[@id="centre_content"]/h2/img/@src')[0]

      numbers = page.xpath('//div[@id="centre_content"]//p[contains(text(),"-")]')[0].text_content()
      if 'tel' in numbers:
        phone = re.findall(r'(.*)tel', numbers)[0].strip().replace(' ', '-').replace("\\xc2", '').replace("\\xa0", '-')
        p.add_contact('phone', phone, None)
      if 'cell' in numbers:
        cell = re.findall(r'(.*)cell', numbers)[0].strip().replace(' ', '-')
        p.add_contact('phone', cell, 'cell')
      if 'fax' in numbers:
        fax = re.findall(r'(.*)fax', numbers)[0].strip().replace(' ', '-')
        p.add_contact('fax', fax, None)

      if len(page.xpath('//div[@id="centre_content"]//a')) > 2:
        site = page.xpath('//div[@id="centre_content"]//a')[-1].attrib['href']
        p.add_link(site, 'personal site')
      yield p

def scrape_mayor(organization):
  mayor_url = 'http://mayor.brantford.ca/Pages/default.aspx'
  page = lxmlize(mayor_url)
  name = re.findall(r'(?<=Mayor)(.*)(?=of)', page.xpath('//div[@id="header"]/h1/text()')[0])[0]

  p = Legislator(name=name, post_id='brantford')
  p.add_source(mayor_url)
  p.add_membership(organization, role='mayor')

  contact_url = page.xpath('.//a[contains(text(),"Contact")]/@href')[0]
  page = lxmlize(contact_url)

  address = ' '.join(page.xpath('//div[@id="main_content"]/p/text()'))
  address = re.sub(r'\s{2,}', ' ', address).strip()
  email = page.xpath('//a[contains(@href, "mailto:")]/@href')[0].split(':')[1]
  phone = page.xpath('//ul[@id="legal_info"]/li[6]/text()')[0].strip().replace('.','-')

  p.add_contact('address', address, 'office')
  p.add_contact('email', email, None)
  p.add_contact('phone', phone, 'office')

  get_links(p, page.xpath('//ul[@id="social_media"]')[0])

  return p

def get_links(councillor, div):
  links = div.xpath('.//a')
  for link in links:
    link = link.attrib['href']

    if 'mailto:' in link:
      continue
    if 'facebook' in link:
      councillor.add_link(link, 'facebook')
    if 'twitter' in link:
      councillor.add_link(link, 'twitter')
    if 'linkedin' in link:
      councillor.add_link(link, 'linkedin')
    if 'google' in link:
      councillor.add_link(link, 'google plus')
    else:
      councillor.add_link(link, 'personal site')
