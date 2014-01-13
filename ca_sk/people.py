from pupa.scrape import Scraper, Legislator

from utils import lxmlize

import re

COUNCIL_PAGE = 'http://www.legassembly.sk.ca/mlas/'


class SaskatchewanPersonScraper(Scraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)

    councillors = page.xpath('//table[@id="MLAs"]//tr')[1:]
    for councillor in councillors:
      name = councillor.xpath('./td')[0].text_content().split('. ')[1]
      district = councillor.xpath('./td')[2].text_content()
      url = councillor.xpath('./td[1]/a/@href')[0]
      page = lxmlize(url)

      p = Legislator(name=name, post_id=district)
      p.add_source(COUNCIL_PAGE)
      p.add_source(url)
      p.role = 'MLA'

      contact = page.xpath('//table[@id="mla-contact"]//tr[2]')[0]
      website = contact.xpath('./td[3]//div[3]//a')
      if website:
        p.add_link(website[0].text_content(), None)

      p.add_contact('address', contact.xpath('./td[1]/div[2]')[0].text_content(), 'legislature')
      p.add_contact('address', ''.join(contact.xpath('./td[2]/div//text()')[1:7]), 'constituency')
      p.add_contact('voice', contact.xpath('./td[1]/div[3]')[0].text_content().split(':')[1].strip().replace('(', '').replace(')', '-'), 'legislature')
      p.add_contact('voice', contact.xpath('./td[2]/div[4]//span/text()')[0].replace('(', '').replace(')', '-'), 'constituency')
      p.add_contact('fax', contact.xpath('./td[1]/div[4]')[0].text_content().split(':')[1].strip().replace('(', '').replace(')', '-'), 'legislature')
      p.add_contact('fax', contact.xpath('./td[2]/div[5]//span/text()')[0].replace('(', '').replace(')', '-'), 'constituency')
      p.add_contact('email', contact.xpath('./td[3]//a[contains(@href, "mailto:")]/text()')[0], None)

      yield p
