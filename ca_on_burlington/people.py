from __future__ import unicode_literals

from pupa.scrape import Scraper

from utils import lxmlize, CanadianLegislator as Legislator

import re

COUNCIL_PAGE = 'http://cms.burlington.ca/Page110.aspx'


class BurlingtonPersonScraper(Scraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)

    councillors = page.xpath('//div[@id="subnav"]//a')
    for councillor in councillors:
      name = councillor.xpath('./span/text()')[0].strip()
      district = councillor.xpath('.//strong')[0].text_content()

      url = councillor.attrib['href']

      if councillor == councillors[0]:
        yield self.scrape_mayor(name, url)
        continue

      page = lxmlize(url)

      address = page.xpath('//div[@id="content"]//p[contains(text(),"City of Burlington,")]')
      contact = page.xpath('//div[@id="subnav"]//p[contains(text(),"Phone")]')[0]
      phone = re.findall(r'Phone: (.*)', contact.text_content())[0].replace('Ext. ', 'x').replace('#', 'x')
      fax = re.findall(r'Fax: (.*)', contact.text_content())[0]
      email = contact.xpath('//a[contains(@href, "mailto:")]')[0].text_content()

      p = Legislator(name=name, post_id=district, role='Councillor')
      p.add_source(COUNCIL_PAGE)
      p.add_source(url)

      p.image = page.xpath('//div[@id="subnav"]//img/@src')[0]

      if address:
        p.add_contact('address', address[0].text_content(), 'legislature')
      p.add_contact('voice', phone, 'legislature')
      p.add_contact('fax', fax, 'legislature')
      p.add_contact('email', email, None)

      yield p

  def scrape_mayor(self, name, url):
    page = lxmlize(url)

    contact = page.xpath('//div[@id="secondary align_RightSideBar"]/blockquote/p/text()')
    phone = contact[0]
    fax = contact[1]
    email = page.xpath('//div[@id="secondary align_RightSideBar"]/blockquote/p/a[contains(@href, "mailto:")]/text()')[0]

    mayor_page = lxmlize('http://www.burlingtonmayor.com')
    contact_url = mayor_page.xpath('//div[@class="menu"]//a[contains(text(),"Contact")]')[0].attrib['href']
    mayor_page = lxmlize(contact_url)
    address = mayor_page.xpath('//div[@class="entry-content"]//p[contains(text(),"City Hall")]')[0].text_content()

    p = Legislator(name=name, post_id="Burlington", role='Mayor')
    p.add_source(COUNCIL_PAGE)
    p.add_source(url)
    p.add_source('http://www.burlingtonmayor.com')

    p.image = page.xpath('//div[@id="secondary align_RightSideBar"]/p/img/@src')[0]
    p.add_contact('voice', phone, 'legislature')
    p.add_contact('fax', fax, 'legislature')
    p.add_contact('email', email, None)
    p.add_contact('address', address, 'legislature')

    return p
