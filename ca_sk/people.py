from pupa.scrape import Scraper, Legislator

from utils import lxmlize, CanadianScraper

import re

COUNCIL_PAGE = 'http://www.legassembly.sk.ca/mlas/'


class SaskatchewanPersonScraper(CanadianScraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)
    organization = self.get_organization()
    yield organization

    councillors = page.xpath('//table[@id="MLAs"]//tr')[1:]
    for councillor in councillors:
      name = councillor.xpath('./td')[0].text_content().split('. ')[1]
      district = councillor.xpath('./td')[2].text_content()
      url = councillor.xpath('./td[1]/a/@href')[0]
      page = lxmlize(url)

      p = Legislator(name=name, post_id=district)
      p.add_source(COUNCIL_PAGE)
      p.add_source(url)
      p.add_membership(organization, role='councillor')

      contact = page.xpath('//table[@id="mla-contact"]//tr[2]')[0]
      office_address = contact.xpath('./td[1]/div[2]')[0].text_content()
      office_phone = contact.xpath('./td[1]/div[3]')[0].text_content().split(':')[1].strip().replace('(', '').replace(')', '-')
      office_fax = contact.xpath('./td[1]/div[4]')[0].text_content().split(':')[1].strip().replace('(', '').replace(')', '-')

      constituency_address = ''.join(contact.xpath('./td[2]/div//text()')[1:7])
      constituency_phone = contact.xpath('./td[2]/div[4]//span/text()')[0].replace('(', '').replace(')', '-')
      constituency_fax = contact.xpath('./td[2]/div[5]//span/text()')[0].replace('(', '').replace(')', '-')

      email = contact.xpath('./td[3]//a[contains(@href, "mailto:")]/text()')[0]
      website = contact.xpath('./td[3]//div[3]//a')
      if website:
        website = website[0].text_content()
        p.add_link(website, 'website')

      p.add_contact('address', office_address, 'Legislative Building')
      p.add_contact('address', constituency_address, 'constituency')
      p.add_contact('phone', office_phone, 'Legislative Building')
      p.add_contact('phone', constituency_phone, 'constituency')
      p.add_contact('fax', office_fax, 'Legislative Building')
      p.add_contact('fax', constituency_fax, 'constituency')
      p.add_contact('email', email, None)

      yield p
