from pupa.scrape import Scraper, Legislator

from utils import lxmlize, CanadianScraper

import re
import urllib
import HTMLParser

COUNCIL_PAGE = 'http://www.ville.levis.qc.ca/Fr/Conseil/'


class LevisPersonScraper(CanadianScraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)

    councillors = page.xpath('//table[@id="Tableau_01"]//a/@href')
    for councillor in councillors:
      page = lxmlize(councillor)
      name = page.xpath('//table[@id="table1"]//td[2]//b')[0].text_content()
      district = page.xpath('//table[@id="table1"]//td[2]//i')[0].text_content()
      if 'Maire' in district:
        district = 'levis'
        role = 'Mayor'
      else:
        district = re.findall(r'[dD]istrict [0-9]{1,2}', district)[0]
        role = 'Councillor'

      p = Legislator(name=name, post_id=district)
      p.add_source(COUNCIL_PAGE)
      p.add_source(councillor)
      p.role = role
      p.image = page.xpath('//img[@alt = "Photo du membre"]/@src')[0]

      script = page.xpath('//table[@id="table1"]//td[2]//script')[0].text_content()
      email = get_email(script)
      p.add_contact('email', email, None)
      yield p


def get_email(script):
  h = HTMLParser.HTMLParser()
  email = h.unescape(re.search('(?<=")[^"]+', urllib.unquote(''.join(re.findall("(?<=\(\')[^']+", script)))).group(0))
  return email + '@ville.levis.qc.ca'
