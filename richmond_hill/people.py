from pupa.scrape import Scraper, Legislator
from larvae.person import Person
from larvae.organization import Organization

from .utils import lxmlize

import re

COUNCIL_PAGE = 'http://www.richmondhill.ca/subpage.asp?pageid=townhall_members_of_the_council'

class Richmond_HillPersonScraper(Scraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)

    councillors = page.xpath('//center/center//a')
    for councillor in councillors:
      name = councillor.text_content()
      url = councillor.attrib['href']
      page = lxmlize(url)
      district = re.findall(r',(.*)-', page.xpath('//div[@class="sectionheading"]')[0].text_content())
      if district:
        district = district[0]
      else:
        district = 'Richmond Hill'

      # print page.xpath()[0].text_content()

      info = page.xpath('//table[2]/tbody/tr/td[2]')
      if info[0].text_content().strip():
        info = info[0].text_content().replace(' - office:', ':')
      else:
        info = page.xpath('//table[2]/tbody/tr/td[3]')[0].text_content().replace(' - office:', ':')

      address = re.findall(r'(?<=Town of Richmond Hill).*(?=Telephone)', info)[0]
      address = re.sub(r'([a-z])([A-Z])', r'\1 \2', address)
      phone = re.findall(r'(?<=Telephone:) (.*)(?=Fax)', info)[0].replace('(','').replace(') ','-').replace(', ext. ', ' x')
      fax = re.findall(r'(?<=Fax:) (.*)(?=E-mail)',info)[0].replace(' ','').replace('(','').replace(')','-')
      email = page.xpath('.//a[contains(@href, "mailto:")]/@href')[0].replace('mailto:', '')

      p = Legislator(name=name, district=district)
      p.add_source(COUNCIL_PAGE)
      p.add_source(url)
      p.add_contact('address', address, None)
      p.add_contact('phone', phone, None)
      p.add_contact('fax', fax, None)
      p.add_contact('email', email, None)

      if 'Website' in info:
        site = re.findall(r'www\..*\.com',info)[0]
        p.add_link(site, 'personal site')
      yield p

      #/html/body/center/table[2]/tbody/tr/td/center/table/tbody/tr/td/table[2]/tbody/tr/td[2]