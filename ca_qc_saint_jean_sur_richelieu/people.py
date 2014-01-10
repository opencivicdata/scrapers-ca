from pupa.scrape import Scraper, Legislator

from utils import lxmlize, CanadianScraper

import re

COUNCIL_PAGE = 'http://www.ville.saint-jean-sur-richelieu.qc.ca/conseil-municipal/membres-conseil/Pages/membres-conseil.aspx'


class SaintJeanSurRichelieuPersonScraper(CanadianScraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)
    organization = self.get_organization()
    yield organization

    councillors = page.xpath('//div[@class="article-content"]//td[@class="ms-rteTableOddCol-0"]')
    for councillor in councillors:

      if not councillor.xpath('.//a'):
        continue
      if 'maire' in councillor.xpath('.//a/@href')[0]:
        yield scrape_mayor(councillor, organization)
        continue

      name = councillor.xpath('.//a')[0].text_content()
      district = councillor.xpath('.//a')[1].text_content()
      url = councillor.xpath('.//a/@href')[0]
      page = lxmlize(url)

      p = Legislator(name=name, post_id=district)
      p.add_source(COUNCIL_PAGE)
      p.add_source(url)
      p.add_membership(organization, role='councillor')

      p.image = councillor.xpath('./preceding-sibling::td//img/@src')[-1]

      contacts = page.xpath('.//td[@class="ms-rteTableOddCol-0"]//text()')
      for contact in contacts:
        if re.findall(r'[0-9]', contact):
          phone = contact.strip().replace(' ', '-')
          p.add_contact('voice', phone, 'office')
      get_links(p, page.xpath('.//td[@class="ms-rteTableOddCol-0"]')[0])
      yield p


def scrape_mayor(div, organization):
  name = div.xpath('.//a')[0].text_content()
  url = div.xpath('.//a/@href')[0]
  page = lxmlize(url)
  contact_url = page.xpath('//a[@title="Joindre le maire"]/@href')[0]
  contact_page = lxmlize(contact_url)

  p = Legislator(name=name, post_id='saint-jean-sur-richelieu')
  p.add_source(COUNCIL_PAGE)
  p.add_source(url)
  p.add_source(contact_url)
  p.add_membership(organization, role='mayor')

  p.image = div.xpath('./preceding-sibling::td//img/@src')[-1]

  contacts = contact_page.xpath('//div[@id="ctl00_PlaceHolderMain_ctl01_ctl01__ControlWrapper_RichHtmlField"]//font/text()')
  address = ' '.join(contacts[:4])
  phone = contacts[-3].split(':')[1].strip().replace(' ', '-')
  fax = contacts[-2].split(':')[1].strip().replace(' ', '-')
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
