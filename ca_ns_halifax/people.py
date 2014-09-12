# coding: utf-8
from pupa.scrape import Scraper

from utils import lxmlize, CanadianLegislator as Legislator

import re

COUNCIL_PAGE = 'http://www.halifax.ca/councillors/index.html'
MAYOR_PAGE = 'http://www.halifax.ca/mayor/'
MAYOR_CONTACT_URL = 'http://www.halifax.ca/mayor/contact.php'


class HalifaxPersonScraper(Scraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE, 'iso-8859-1')
    nodes = page.xpath('//table[@width="484"]//tr')
    try:
      for district_row, councillor_row, contact_row, _ in chunks(nodes, 4):
        post_id = district_row.xpath('string(.//strong)')
        name = councillor_row.xpath('string(.)')[len('Councillor '):]
        # TODO: phone numbers on site don't include area code. Add manually?
        #phone = contact_row.xpath('string(td[2]/text())')
        email = contact_row.xpath('string(td[4]/a)').replace('[at]', '@')

        p = Legislator(name=name, post_id=post_id, role='Councillor')
        p.add_source(COUNCIL_PAGE)
        #p.add_contact('voice', phone, 'legislature')
        p.add_contact('email', email, None)
        yield p
    except ValueError:
      # on the last run through, there will be less than 4 rows to unpack
      pass

    mayor_page = lxmlize(MAYOR_PAGE, 'iso-8859-1')
    name = mayor_page.xpath('string(//h1[contains(., "Bio")])')[:-len(' Bio')]
    contact_page = lxmlize(MAYOR_CONTACT_URL, 'iso-8859-1')
    email = contact_page.xpath('string(//a[contains(., "@")][1])')

    p = Legislator(name=name, post_id='Halifax', role='Councillor')
    p.add_source(MAYOR_PAGE)
    p.add_source(MAYOR_CONTACT_URL)
    p.add_contact('email', email, None)
    yield p


def chunks(l, n):
  """ Yield successive n-sized chunks from l.
  """
  for i in xrange(0, len(l), n):
    yield l[i:i + n]
