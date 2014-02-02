from pupa.scrape import Scraper, Legislator

from utils import lxmlize

import re

COUNCIL_PAGE = 'http://www.brantford.ca/govt/council/members/Pages/default.aspx'


class BrantfordPersonScraper(Scraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)

    yield scrape_mayor()

    councillors = page.xpath('//div[@id="centre_content"]//tr')
    for councillor in councillors:
      if 'Position' in councillor.text_content():
        continue

      district = councillor.xpath('./td')[0].text_content().replace('Councillor', '')
      name = councillor.xpath('./td')[1].text_content()
      url = councillor.xpath('./td/a')[0].attrib['href']

      p = Legislator(name=name, post_id=district, role='Councillor')
      p.add_source(COUNCIL_PAGE)
      p.add_source(url)

      page = lxmlize(url)

      address = page.xpath('//div[@id="centre_content"]//p')[0].text_content().replace("\r\n", ', ')
      email = page.xpath('//a[contains(@href,"mailto:")]')[0].attrib['href'].replace('mailto:', '')
      p.add_contact('address', address, 'legislature')
      p.add_contact('email', email, None)

      p.image = page.xpath('//div[@id="centre_content"]//img/@src')[0]

      numbers = page.xpath('//div[@id="centre_content"]//p[contains(text(),"-")]')[0].text_content()
      if 'tel' in numbers:
        phone = re.findall(r'(.*)tel', numbers)[0].strip().replace(' ', '-').replace("\\xc2", '').replace("\\xa0", '-')
        p.add_contact('voice', phone, 'legislature')
      if 'cell' in numbers:
        cell = re.findall(r'(.*)cell', numbers)[0].strip().replace(' ', '-')
        p.add_contact('cell', cell, 'legislature')
      if 'fax' in numbers:
        fax = re.findall(r'(.*)fax', numbers)[0].strip().replace(' ', '-')
        p.add_contact('fax', fax, 'legislature')

      if len(page.xpath('//div[@id="centre_content"]//a')) > 2:
        p.add_link(page.xpath('//div[@id="centre_content"]//a')[-1].attrib['href'], None)
      yield p


def scrape_mayor():
  mayor_url = 'http://mayor.brantford.ca/Pages/default.aspx'
  page = lxmlize(mayor_url)
  name = re.findall(r'(?<=Mayor )(.*)(?=\r)', page.xpath('//div[@id="main_content"]/h1/text()')[0])[0]

  p = Legislator(name=name, post_id='Brantford', role='Mayor')
  p.add_source(mayor_url)

  contact_url = page.xpath('.//a[contains(text(),"Contact")]/@href')[0]
  page = lxmlize(contact_url)

  address = ' '.join(page.xpath('//div[@id="main_content"]/p/text()'))
  address = re.sub(r'\s{2,}', ' ', address).strip()
  email = page.xpath('//a[contains(@href, "mailto:")]/@href')[0].split(':')[1]
  phone = page.xpath('//ul[@id="legal_info"]/li[6]/text()')[0].strip().replace('.', '-')

  p.add_contact('address', address, 'legislature')
  p.add_contact('email', email, None)
  p.add_contact('voice', phone, 'legislature')

  get_links(p, page.xpath('//ul[@id="social_media"]')[0])

  return p


def get_links(councillor, div):
  links = div.xpath('.//a')
  for link in links:
    link = link.attrib['href']

    if 'mailto:' in link:
      continue
    else:
      councillor.add_link(link, None)
