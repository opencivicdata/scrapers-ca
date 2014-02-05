# coding: utf-8
from pupa.scrape import Scraper, Legislator

from utils import lxmlize

import re

COUNCIL_PAGE = 'http://app.toronto.ca/im/council/councillors.jsp'


class TorontoPersonScraper(Scraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)

    for a in page.xpath('//a[contains(@href,"councillors/")]'):
      if 'vacant' in a.attrib['href']:
        continue
      yield self.scrape_councilor(a.attrib['href'])

    a = page.xpath('//a[contains(@href,"mayor")]')[0]
    yield self.scrape_mayor(a.attrib['href'])

  def scrape_councilor(self, url):
    page = lxmlize(url)
    info = page.xpath("//div[@class='single-item']")[0]
    name = info.xpath(".//h1")[0].text_content().replace('Councillor', '').strip()
    if name.startswith("Ana Bail"):
      name = u"Ana Bailão"
    district = info.xpath(".//p|.//h3")[0].text_content()
    district = re.sub('\A(Ward \d+).+\Z', '\g<1>', district)

    p = Legislator(name=name, post_id=district, role='Councillor')
    p.add_source(COUNCIL_PAGE)
    p.add_source(url)

    info = info.xpath(".//table")[0]

    p.image = info.xpath('.//img/@src')[0]

    if "Facebook" in info.text_content():
      p.add_link(info.xpath('.//a[contains(@href, "facebook.com")]')[0].attrib['href'], None)

    if "Twitter" in info.text_content():
      p.add_link(info.xpath('.//a[contains(@href,"twitter.com")]')[0].attrib['href'], None)

    p.add_contact('email', info.xpath('.//a[contains(@href,"mailto:")]')[0].text_content(), None)
    contacts = info.xpath('.//p[text()[contains(.,"Phone:")]]')
    for contact in contacts:
      lines = [line.strip() for line in contact.xpath('.//text()')]

      note = contact.getprevious()
      if note is not None and len(note.xpath('.//text()')) == 1:
        note = note.text_content()
      else:
        note = lines.pop(0)

      if note in ('Toronto City Hall', 'Office of the Deputy Mayor:'):
        note = 'legislature'
      elif note in ('Constituency Office', 'Constituency Office:', 'Community Office', 'East York Civic Centre Office'):
        note = 'constituency'
      else:
        print 'Unexpected contact_details.note: %s' % note
        raise Exception('Unexpected contact_details.note: %s' % note)

      address_block = True
      address_lines = []
      for line in lines:
        if line.startswith('Phone:'):
          address_block = False
          p.add_contact('voice', line.replace("Phone:", '').strip(), note)
        elif line.startswith('Fax:'):
          address_block = False
          p.add_contact('fax', line.replace("Fax:", '').strip(), note)
        elif line.startswith('Constituency Office:'):
          address_block = False
          p.add_contact('voice', line.replace("Phone:", '').strip(), 'constituency')
        elif line.startswith('Constituency Fax:'):
          address_block = False
          p.add_contact('fax', line.replace("Fax:", '').strip(), 'constituency')
        elif address_block:
          address_lines.append(line)
        else:
          raise Exception('Unexpected contact detail: %s' % line)

      if address_lines:
        p.add_contact('address', '\n'.join(address_lines), note)
    return p

  def scrape_mayor(self, url):
    page = lxmlize(url)
    name = page.xpath("//div[@class='detail']//h1/text()")[0].replace("Toronto Mayor", "").strip()

    p = Legislator(name, post_id="Toronto", role='Mayor')
    p.add_source(COUNCIL_PAGE)
    p.add_source(url)

    p.image = page.xpath('//div[@class="image"]/img/@src')[0]

    url = page.xpath('//a[contains(text(), "Contact the Mayor")]')[0].attrib['href']
    url = url.replace('www.', 'www1.') # @todo fix lxmlize to use the redirected URL to make links absolute
    p.add_source(url)
    page = lxmlize(url)

    info = page.xpath('//div[@class="detail"]')[0]
    address = ''.join(info.xpath('.//p/text()')[0:6]).replace(",,", ",")
    phone = info.xpath('.//p[3]/text()')[0]

    p.add_contact('address', address, 'legislature')
    p.add_contact('voice', phone, 'legislature')
    return p
