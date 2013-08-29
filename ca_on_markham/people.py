from pupa.scrape import Scraper, Legislator
from pupa.models import Person
from pupa.models import Organization

from utils import lxmlize, CanadianScraper

import re

COUNCIL_PAGE = 'http://www.markham.ca/wps/portal/Markham/MunicipalGovernment/MayorAndCouncil/RegionalAndWardCouncillors/!ut/p/a1/04_Sj9CPykssy0xPLMnMz0vMAfGjzOJN_N2dnX3CLAKNgkwMDDw9XcJM_VwCDUMDDfULsh0VAfz7Fis!/'


class MarkhamPersonScraper(CanadianScraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)
    organization = self.get_organization()
    yield organization

    mayor_url = page.xpath('//a[contains(text(), "Office of the Mayor")]/@href')[0]
    yield scrape_mayor(mayor_url, organization)

    councillors = page.xpath('//div[@class="interiorContentWrapper"]//td')
    for councillor in councillors:
      if not councillor.text_content().strip() or "Address" in councillor.text_content():
        continue
      if not councillor.xpath('.//a'):
        break
      name = councillor.xpath('.//strong')[1].text_content().strip()
      district = councillor.xpath('.//a//text()')[0].strip()
      if 'Ward' in district:
        district = district.replace('Councillor', '')
        role = 'councillor'
      else:
        role = district
        district = 'Markham'

      image = councillor.xpath('.//img/@src')[0]
      url = councillor.xpath('.//a/@href')[0]

      if 'Ward 4' in district:
        yield scrape_4(name, url, organization, image)
        continue

      page = lxmlize(url)

      p = Legislator(name=name, post_id=district)
      p.add_source(COUNCIL_PAGE)
      p.add_source(url)
      p.add_membership(organization, role=role)

      p.image = image

      contact = page.xpath('//div[@class="microSiteLinksWrapper"]')[1]
      address = re.sub(r'\s{2,}', ' ', ' '.join(contact.xpath('.//p/text()')[:2])).strip()
      phone = contact.xpath('.//p/text()')[2].split(':')[1].strip()
      email = contact.xpath('.//a[contains(@href,"mailto:")]/text()')[0]
      website = contact.xpath('.//a[not( contains(@href, "mailto:"))]/text()')
      if website:
        p.add_link(website[0], 'personal site')
      p.add_contact('address', address, 'office')
      p.add_contact('phone', phone, 'office')
      p.add_contact('email', email, None)

      get_links(p, contact)
      yield p


def scrape_4(name, url, organization, image):
  page = lxmlize(url)

  p = Legislator(name=name, post_id='Ward 4')
  p.add_source(url)
  p.add_source(COUNCIL_PAGE)
  p.add_membership(organization, role='councillor')

  address = re.sub(r'\s{2,}', ' ', ' '.join(page.xpath('//div[@class="interiorContentWrapper"]/p[3]/text()')))
  phone = page.xpath('//div[@class="interiorContentWrapper"]/p[4]/text()')[0].split(':')[1].strip()
  email = page.xpath('//a[contains(@href, "mailto:")]/text()')[0]
  p.add_contact('address', address, 'office')
  p.add_contact('phone', phone, 'office')
  p.add_contact('email', email, 'office')
  p.image = image
  return p


def scrape_mayor(url, organization):
  page = lxmlize(url)
  name = page.xpath('//div[@class="interiorContentWrapper"]/p/strong/text()')[0]
  address = ' '.join(page.xpath('//div[@class="interiorContentWrapper"]/p/text()')[1:3])
  address = re.sub(r'\s{2,}', ' ', address)
  phone = page.xpath('//div[@class="interiorContentWrapper"]/p/text()')[3].split(':')[1].strip()
  email = page.xpath('//a[contains(@href, "mailto:")]/text()')[0]

  p = Legislator(name=name, post_id='markham')
  p.add_source(url)
  p.add_membership(organization, 'mayor')
  p.add_contact('address', address, 'office')
  p.add_contact('phone', phone, 'office')
  p.add_contact('email', email, None)
  yield p


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
