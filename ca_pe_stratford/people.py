from pupa.scrape import Scraper

from utils import lxmlize, CanadianLegislator as Legislator

import re

COUNCIL_PAGE = 'http://www.townofstratford.ca/town-hall/government/town-council/'


class StratfordPersonScraper(Scraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE, user_agent='Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)')

    yield self.scrape_mayor(page)

    councillors = page.xpath('//strong[contains(text(), "Councillor")]/parent::p|//b[contains(text(), "Councillor")]/parent::p')
    for councillor in councillors:

      name = councillor.xpath('./strong/text()|./b/text()')[0].replace('Councillor', '').strip()
      district = re.findall('(?<=Ward \d, ).*', councillor.text_content())[0].strip()

      p = Legislator(name=name, post_id=district, role='Councillor')
      p.add_source(COUNCIL_PAGE)

      p.image = councillor.xpath('.//img/@src')[0]

      phone = re.findall(r'Phone(.*)', councillor.text_content())
      node = councillor
      while not phone:
        node = node.xpath('./following-sibling::p')[1]
        phone = re.findall(r'Phone(.*)', node.text_content())
      phone = phone[0].strip()

      email = councillor.xpath('.//a[contains(@href, "mailto:")]')
      if not email:
        email = councillor.xpath('./following-sibling::p//a[contains(@href, "mailto")]')
      email = email[0].text_content()

      if len(re.sub(r'\D', '', phone)) == 7:
        phone = '902-%s' % phone
      p.add_contact('voice', phone, 'legislature')
      p.add_contact('email', email, None)

      yield p

  def scrape_mayor(self, page):
    info = page.xpath('//div[@class="entry-content"]/p')[:4]
    name = info[0].text_content().replace('Mayor', '')
    email = info[2].xpath('./a')[0].text_content()
    phone = info[3].text_content().replace('Phone ', '')

    p = Legislator(name=name, post_id='Stratford', role='Mayor')
    p.add_source(COUNCIL_PAGE)
    p.image = page.xpath('//div[@class="entry-content"]/p/a/img/@src')[0]
    p.add_contact('email', email, None)
    if len(re.sub(r'\D', '', phone)) == 7:
      phone = '902-%s' % phone
    p.add_contact('voice', phone, 'legislature')
    return p
