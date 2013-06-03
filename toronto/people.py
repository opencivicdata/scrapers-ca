from pupa.scrape import Scraper, Legislator
from larvae.person import Person
from larvae.organization import Organization

from .utils import lxmlize

import re

COUNCIL_PAGE = 'http://app.toronto.ca/im/council/councillors.jsp'

class TorontoPersonScraper(Scraper):
  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)

    a = page.xpath('//a[contains(@href,"mayor")]')[0]
    yield self.scrape_mayor(a.attrib['href'])

    for a in page.xpath('//a[contains(@href,"councillors/")]'):
      yield self.scrape_councilor(a.attrib['href'])

  def scrape_councilor(self, url):
    page = lxmlize(url)
    info = page.xpath("//div[@class='main']")[0]
    name = info.xpath("//h3")[1].text_content().replace('Councillor', '').strip()
    district = info.xpath("//p")[0].text_content()

    p = Legislator(name=name, district=district)

    info = info.xpath("//div[@class='last']")[0]

    # add links
    p.add_source(COUNCIL_PAGE)
    p.add_source(url)

    if "website:" in info.text_content():
      p.add_link(info.xpath('.//a')[1].attrib['href'], 'homepage')

    if "Facebook" in info.text_content():
      p.add_link(info.xpath('//a[contains(@href, "facebook.com")]')[0].attrib['href'], 'facebook')

    if "Twitter" in info.text_content():
      p.add_link(info.xpath('//a[contains(@href,"twitter.com")]')[0].attrib['href'], 'twitter')

    # add contact info
    p.add_contact('email', info.xpath('.//a')[0].text_content(),'')
   #//*[@id="content"]/div/div[1]/div[2]/p[1]
    contacts = info.xpath('//div/p[text()[contains(.,"Phone:")]]')
    for contact in contacts:
      note = contact.xpath('.//strong')[0].text_content()
      contact = contact.xpath('br/following-sibling::node()')
      if len(contact) > 8 : continue
      if len(contact) >= 4:
        address = (contact[0]+", "+contact[2]).strip()
        p.add_contact('address', address, note)
        if "Phone: " in contact[4]:
          phone = contact[4].replace("Phone: ",'').strip()
          p.add_contact('phone', phone, note)
        if len(contact) > 5 and "Fax:" in contact[6]:
          fax = contact[6].replace("Fax: ",'').strip()
          p.add_contact('fax', fax, note)
      else:
        phone = contact[0].strip()
        p.add_contact('phone', phone, note)
        fax = contact[2].strip()
        p.add_contact('fax', fax, note)
    return p

  def scrape_mayor(self, url):
    page = lxmlize(url)
    name = page.xpath("//div[@class='detail']//h1/text()")[0].replace("Toronto Mayor", "").strip()
    p = Legislator(name, "Toronto")

    p.add_source(COUNCIL_PAGE)
    p.add_source(url)

    url = page.xpath('//a[contains(text(), "Contact the Mayor")]')[0].attrib['href']
    p.add_source(url)
    page = lxmlize(url)

    info = page.xpath('//div[@class="detail"]')[0]
    address = (', ').join(info.xpath('.//p/text()')[0:6]).replace(",,", ",")
    phone = info.xpath('.//p[3]/text()')[0]

    p.add_contact('address', address, 'Mailing')
    p.add_contact('phone', phone, '')
    return p
