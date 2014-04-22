from pupa.scrape import Scraper

from utils import lxmlize, CanadianLegislator as Legislator

import re

COUNCIL_PAGE = 'http://www.legassembly.sk.ca/mlas/'


class SaskatchewanPersonScraper(Scraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)

    councillors = page.xpath('//table[@id="MLAs"]//tr')[1:]
    for councillor in councillors:
      name = councillor.xpath('./td')[0].text_content().split('. ', 1)[1]
      party = councillor.xpath('./td')[1].text
      district = councillor.xpath('./td')[2].text_content()
      url = councillor.xpath('./td[1]/a/@href')[0]
      page = lxmlize(url)

      p = Legislator(name=name, post_id=district, role='MLA', party=party)
      p.add_source(COUNCIL_PAGE)
      p.add_source(url)

      contact = page.xpath('//table[@id="mla-contact"]//tr[2]')[0]
      website = contact.xpath('./td[3]//div[3]//a')
      if website:
        p.add_link(website[0].text_content(), None)

      p.add_contact('address', contact.xpath('./td[1]/div[2]')[0].text_content(), 'legislature')
      p.add_contact('address', ''.join(contact.xpath('./td[2]/div//text()')[1:7]), 'constituency')
      numbers = [
        contact.xpath('./td[1]/div[3]')[0].text_content().split(':')[1].strip(),
        contact.xpath('./td[2]/div[4]//span/text()')[0],
        contact.xpath('./td[1]/div[4]')[0].text_content().split(':')[1].strip(),
        contact.xpath('./td[2]/div[5]//span/text()')[0],
      ]
      for index, number in enumerate(numbers):
        if len(number) < 10:
          numbers[index] = '306-%s' % number
      p.add_contact('voice', numbers[0], 'legislature')
      p.add_contact('voice', numbers[1], 'constituency')
      p.add_contact('fax', numbers[2], 'legislature')
      p.add_contact('fax', numbers[3], 'constituency')
      p.add_contact('email', contact.xpath('./td[3]//a[contains(@href, "mailto:")]/text()')[0], None)

      yield p
