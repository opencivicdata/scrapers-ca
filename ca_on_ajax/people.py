from pupa.scrape import Scraper, Legislator

from utils import lxmlize

import re

COUNCIL_PAGE = 'http://www.ajax.ca/en/insidetownhall/mayorcouncillors.asp'

class AjaxPersonScraper(Scraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)

    councillors = page.xpath('//ul[@class="subNav top"]/li/ul//li/a')
    for councillor in councillors:
      name = councillor.text_content()

      url = councillor.attrib['href']
      page = lxmlize(url)

      if councillor == councillors[0]:
        district = 'Ajax'
      else:
        district = re.findall(r'Ward.*', page.xpath('//div[@id="printAreaContent"]//h1')[0].text_content())[0]

      p = Legislator(name=name, post_id=district)
      p.add_source(COUNCIL_PAGE)
      p.add_source(url)

      contact_info = page.xpath('//table[@class="datatable"][1]//tr')[1:]
      for line in contact_info:
        contact_type = line.xpath('./td')[0].text_content().strip()
        contact = line.xpath('./td')[1].text_content().strip()
        if re.match(r'(Phone)|(Fax)|(Email)' , contact_type):
          p.add_contact(contact_type, contact, None)
        else:
          p.add_link(contact, contact_type)
      yield p