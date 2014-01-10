from pupa.scrape import Scraper, Legislator

from utils import lxmlize, CanadianScraper

import re

COUNCIL_PAGE = 'http://www.richmondhill.ca/subpage.asp?pageid=townhall_members_of_the_council'


class RichmondHillPersonScraper(CanadianScraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)
    organization = self.get_organization()
    yield organization

    councillors = page.xpath('//center/center//a')
    for councillor in councillors:
      name = councillor.text_content().strip()
      url = councillor.attrib['href']
      page = lxmlize(url)
      district = re.findall(r',(.*)-', page.xpath('//div[@class="sectionheading"]')[0].text_content())
      if district:
        district = district[0]
        role = 'councillor'
      else:
        district = 'Richmond Hill'
        role = 'mayor'
      # print page.xpath()[0].text_content()

      info = page.xpath('//table[2]/tbody/tr/td[2]')
      if info[0].text_content().strip():
        info = info[0].text_content().replace(' - office:', ':')
      else:
        info = page.xpath('//table[2]/tbody/tr/td[3]')[0].text_content().replace(' - office:', ':')

      address = re.findall(r'(?<=Town of Richmond Hill).*(?=Telephone)', info)[0]
      address = re.sub(r'([a-z])([A-Z])', r'\1 \2', address)
      phone = re.findall(r'(?<=Telephone:) (.*)(?=Fax)', info)[0].replace('(', '').replace(') ', '-').replace(', ext. ', ' x')
      fax = re.findall(r'(?<=Fax:) (.*)(?=E-mail)', info)[0].replace(' ', '').replace('(', '').replace(')', '-')
      email = page.xpath('.//a[contains(@href, "mailto:")]/@href')[0].replace('mailto:', '')

      p = Legislator(name=name, post_id=district)
      p.add_source(COUNCIL_PAGE)
      p.add_source(url)
      p.add_membership(organization, role=role)
      p.add_contact('address', address, 'office')
      p.add_contact('voice', phone, 'office')
      p.add_contact('fax', fax, 'office')
      p.add_contact('email', email, None)
      p.image = page.xpath('//img[contains(@alt, "%s")]/@src' % name)[0]
      if 'Website' in info:
        site = re.findall(r'www\..*\.com', info)[0]
        p.add_link(site, 'personal site')
      yield p

      #/html/body/center/table[2]/tbody/tr/td/center/table/tbody/tr/td/table[2]/tbody/tr/td[2]
