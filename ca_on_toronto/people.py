from pupa.scrape import Scraper, Legislator

from utils import lxmlize, CanadianScraper

import re

COUNCIL_PAGE = 'http://app.toronto.ca/im/council/councillors.jsp'


class TorontoPersonScraper(CanadianScraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)
    organization = self.get_organization()
    yield organization

    a = page.xpath('//a[contains(@href,"mayor")]')[0]
    yield self.scrape_mayor(a.attrib['href'], organization)

    for a in page.xpath('//a[contains(@href,"councillors/")]'):
      if 'vacant' in a.attrib['href']:
        continue
      yield self.scrape_councilor(a.attrib['href'], organization)

  def scrape_councilor(self, url, organization):
    page = lxmlize(url)
    info = page.xpath("//div[@class='main']")[0]
    name = info.xpath("//h3")[1].text_content().replace('Councillor', '').strip()
    if "Ana Bail" in name:
      name = "Ana Bailao"
    district = info.xpath("//p")[0].text_content()

    p = Legislator(name=name, post_id=district)

    info = info.xpath("//div[@class='last']")[0]

    # add links
    p.add_source(COUNCIL_PAGE)
    p.add_source(url)
    p.add_membership(organization, role='councillor')

    p.image = page.xpath('//div[@class="two_column"]/div/img/@src')[0]

    if "website:" in info.text_content():
      p.add_link(info.xpath('.//a')[1].attrib['href'], None)

    if "Facebook" in info.text_content():
      p.add_link(info.xpath('//a[contains(@href, "facebook.com")]')[0].attrib['href'], None)

    if "Twitter" in info.text_content():
      p.add_link(info.xpath('//a[contains(@href,"twitter.com")]')[0].attrib['href'], None)

    # add contact info
    p.add_contact('email', info.xpath('.//a')[0].text_content(), None)
   #//*[@id="content"]/div/div[1]/div[2]/p[1]
    contacts = info.xpath('//div/p[text()[contains(.,"Phone:")]]')
    for contact in contacts:
      note = contact.xpath('.//strong')[0].text_content()
      contact = contact.xpath('br/following-sibling::node()')
      if len(contact) > 8:
        continue
      if len(contact) >= 4:
        address = (contact[0] + ", " + contact[2]).strip()
        p.add_contact('address', address, note)
        if "Phone: " in contact[4]:
          phone = contact[4].replace("Phone: ", '').strip()
          p.add_contact('voice', phone, note)
        if len(contact) > 5 and "Fax:" in contact[6]:
          fax = contact[6].replace("Fax: ", '').strip()
          p.add_contact('fax', fax, note)
      else:
        phone = contact[0].strip()
        p.add_contact('voice', phone, note)
        fax = contact[2].strip()
        p.add_contact('fax', fax, note)
    return p

  def scrape_mayor(self, url, organization):
    page = lxmlize(url)
    name = page.xpath("//div[@class='detail']//h1/text()")[0].replace("Toronto Mayor", "").strip()

    p = Legislator(name, "Toronto")
    p.add_source(COUNCIL_PAGE)
    p.add_source(url)
    p.add_membership(organization, role='mayor')

    p.image = page.xpath('//div[@class="image"]/img/@src')[0]

    url = page.xpath('//a[contains(text(), "Contact the Mayor")]')[0].attrib['href']
    p.add_source(url)
    page = lxmlize(url)

    info = page.xpath('//div[@class="detail"]')[0]
    address = (', ').join(info.xpath('.//p/text()')[0:6]).replace(",,", ",")
    phone = info.xpath('.//p[3]/text()')[0]

    p.add_contact('address', address, 'legislature')
    p.add_contact('voice', phone, 'legislature')
    return p
