from pupa.scrape import Scraper

from utils import lxmlize, CanadianLegislator as Legislator

import re

COUNCIL_PAGE = 'http://www.whitby.ca/en/townhall/meetyourcouncil.asp'


class WhitbyPersonScraper(Scraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)

    person_elems = page.xpath('//tr')
    for person in person_elems:
      info = person[1]
      try: # Mayor and regional councillors
        name, role = info[0].text_content().split(',')
        role = role.strip()
        post_id = 'Whitby'
      except ValueError:
        post_id = ' '.join(info[0].text_content().split()[:2])
        name, role = info[1].text_content().split(', ')
      email = info.xpath('string(.//a/@href)')[len('mailto:'):].split(';')[0]
      image = person.xpath('string(.//img/@src)')
      p = Legislator(name=name, post_id=post_id, role=role, image=image)
      p.add_source(COUNCIL_PAGE)
      p.add_contact('email', email, None)
      yield p
      
