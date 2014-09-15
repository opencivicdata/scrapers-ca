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
      p.image = page.xpath('string(//div[contains(@class, "mla-image-cell")]/img/@src)')

      contact = page.xpath('//div[@id="mla-contact"]/div[2]')[0]
      website = contact.xpath('./div[3]/div[3]/div[2]/a')
      if website:
        p.add_link(website[0].text_content(), None)

      p.add_contact('address', ' '.join(contact.xpath('.//div[@class="col-md-4"][2]/div//text()')[1:9]), 'constituency')
      phone_leg = contact.xpath('string(.//span[@id="MainContent_ContentBottom_Property6"]//text())')
      phone_const = contact.xpath('string(.//div[@class="col-md-4"]/div[4]/span/span/text())')
      p.add_contact('voice', phone_leg, 'legislature')
      p.add_contact('voice', phone_const, 'constituency')
      email = contact.xpath('string(.//a[contains(@href, "mailto:")]/text())')
      p.add_contact('email', email, None)

      yield p
