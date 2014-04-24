from __future__ import unicode_literals

from pupa.scrape import Scraper

from utils import lxmlize, CanadianLegislator as Legislator

import re

COUNCIL_PAGE = 'http://www.ville.saint-jean-sur-richelieu.qc.ca/conseil-municipal/membres-conseil/Pages/membres-conseil.aspx'


class SaintJeanSurRichelieuPersonScraper(Scraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)

    councillors = page.xpath('//div[@class="article-content"]//td[@class="ms-rteTableOddCol-0"]')
    yield scrape_mayor(councillors[0])
    for councillor in councillors[1:]:
      if not councillor.xpath('.//a'):
        continue

      name = councillor.xpath('.//a')[0].text_content().strip()
      district = councillor.xpath('.//a')[1].text_content()
      url = councillor.xpath('.//a/@href')[0]
      page = lxmlize(url)

      p = Legislator(name=name, post_id=district, role='Conseiller')
      p.add_source(COUNCIL_PAGE)
      p.add_source(url)

      p.image = councillor.xpath('./preceding-sibling::td//img/@src')[-1]

      contacts = page.xpath('.//td[@class="ms-rteTableOddCol-0"]//text()')
      for contact in contacts:
        if re.findall(r'[0-9]', contact):
          phone = contact.strip().replace(' ', '-')
          p.add_contact('voice', phone, 'legislature')
      get_links(p, page.xpath('.//td[@class="ms-rteTableOddCol-0"]')[0])

      email = page.xpath(
        'string(//a[contains(@href, "mailto:")]/@href)')[len('mailto:'):]
      p.add_contact('email', email, None)
      yield p


def scrape_mayor(div):
  name = div.xpath('.//a')[0].text_content()
  url = div.xpath('.//a/@href')[0]
  page = lxmlize(url)
  contact_url = page.xpath('//a[@title="Joindre le maire"]/@href')[0]
  contact_page = lxmlize(contact_url)

  p = Legislator(name=name, post_id='Saint-Jean-sur-Richelieu', role='Maire')
  p.add_source(COUNCIL_PAGE)
  p.add_source(url)
  p.add_source(contact_url)

  p.image = div.xpath('./preceding-sibling::td//img/@src')[-1]

  contacts = contact_page.xpath('//div[@id="ctl00_PlaceHolderMain_ctl01_ctl01__ControlWrapper_RichHtmlField"]//font/text()')
  address = ' '.join(contacts[:4])
  phone = contacts[-3].split(':')[1].strip().replace(' ', '-')
  fax = contacts[-2].split(':')[1].strip().replace(' ', '-')
  # mayor's email is a form
  return p


def get_links(councillor, div):
  links = div.xpath('.//a')
  for link in links:
    link = link.attrib['href']

    if 'mailto:' in link:
      continue
    else:
      councillor.add_link(link, None)
