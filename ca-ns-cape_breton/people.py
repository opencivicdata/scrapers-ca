from pupa.scrape import Scraper, Legislator
from larvae.person import Person
from larvae.organization import Organization

from utils import lxmlize

import re

COUNCIL_PAGE = 'http://www.cbrm.ns.ca/councillors.html'

class Cape_BretonPersonScraper(Scraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)

    councillors = page.xpath('//table[@class="table_style"]/tbody/tr')[1:]
    for councillor in councillors:
       name = councillor.xpath('.//a')[0].text_content()
       district = councillor.xpath('.//strong')[0].text_content()

       address = councillor.xpath('.//td')[3].text_content().replace("\r\n",', ')
       phone = councillor.xpath('.//td[5]/p/text()')[0].split(':')[1].replace("(",'').replace(") ",'-')
       fax = councillor.xpath('.//td[5]/p/text()')[1].split(':')[1].replace("(",'').replace(") ",'-')

       p = Legislator(name=name, post_id=district)
       p.add_source(COUNCIL_PAGE)
       p.add_contact('address', address, None)
       p.add_contact('phone', phone, None)
       p.add_contact('fax', fax, None)
       yield p