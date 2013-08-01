from pupa.scrape import Scraper, Legislator
from larvae.person import Person
from larvae.organization import Organization

from .utils import lxmlize

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
      phone = re.findall(r'Phone: (.*)', contact.text_content())[0].replace('Ext. ', 'x').replace('#','x')
      fax = re.findall(r'Fax: (.*)', contact.text_content())[0]
      email = contact.xpath('//a[contains(@href, "mailto:")]')[0].text_content()
      
      p = Legislator(name=name, district=district)
      p.add_source(COUNCIL_PAGE)
      p.add_source(url)
      if address:
        p.add_contact('address', address[0].text_content(), None)
      p.add_contact('phone', phone, None)
      p.add_contact('fax', fax, None)
      p.add_contact('email', email, None)

      link_div = contact.xpath('following-sibling::p')[0]
      self.get_links(p, link_div)
      yield p
  def scrape_mayor(self, name, url):
    page = lxmlize(url)

    contact = page.xpath('//div[@id="grey-220"]//li')[0]
    
    phone = re.findall(r'[0-9]{3}-[0-9]{3}-[0-9]{4}', contact.text_content())[0].replace('Ext. ', 'x')
    fax = re.findall(r'Fax: (.*)', contact.text_content())[0]
    email = contact.xpath('//a[contains(@href, "mailto:")]')[0].text_content()

    link_div = page.xpath('//div[@id="leftnav-grey"]')[0]

    mayor_page = lxmlize('http://www.burlingtonmayor.com')
    contact_url = mayor_page.xpath('//div[@class="menu"]//a[contains(text(),"Contact")]')[0].attrib['href']
    mayor_page = lxmlize(contact_url)
    address = mayor_page.xpath('//div[@class="entry-content"]//p[contains(text(),"City Hall")]')[0].text_content()

    p = Legislator(name=name, district="Burlington")
    p.add_source(COUNCIL_PAGE)
    p.add_source(url)
    p.add_source('http://www.burlingtonmayor.com')
    p.add_contact('phone', phone, None)
    p.add_contact('fax', fax, None)
    p.add_contact('email', email, None)
    p.add_contact('address', address, None)



    self.get_links(p, link_div)

    return p

  def get_links(self, councillor, div):
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