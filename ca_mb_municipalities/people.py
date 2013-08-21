from pupa.scrape import Scraper, Legislator

from utils import lxmlize

import re

COUNCIL_PAGE = 'http://web5.gov.mb.ca/Public/municipalities.aspx'


class ManitobaPersonScraper(Scraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)

    districts = page.xpath('//div[@id="ctl00_PublicContent_divSearchContent"]//tr')[5::3]
    for district in districts:
      title = district.xpath('.//td//text()')
      if len(title[0]) > 1:
        title = title[0]
      else:
        title = ''.join(title[:2])

        contact = district.xpath('.//td/text()')
        address = ' '.join(contact[:4])
        address = re.sub(r'(Fax:.*)', '', address).strip()
        fax = contact[4].split(':')[1].strip()
        if not fax:
          fax = contact[3].split(':')[1].strip()

        phone = district.xpath('.//b[contains(text(), "Phone")]/text()')[0].split(':')[1].strip()
        email = district.xpath('.//a[contains(@href, "mailto:")]/text()')[0].strip()

        councillors = district.xpath('.//td[3]/text()')
        for councillor in councillors:
          p = Legislator(name=councillor, post_id=title)
          p.add_source(COUNCIL_PAGE)
          p.add_contact('address', address, None)
          p.add_contact('fax', fax, None)
          p.add_contact('phone', phone, None)
          p.add_contact('email', email, None)
          yield p