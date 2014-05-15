from pupa.scrape import Scraper

from utils import lxmlize, CanadianLegislator as Legislator

import re

COUNCIL_PAGE = 'http://www.clarington.net/index.php?content=townhall/council'


class ClaringtonPersonScraper(Scraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)

    for person_header_elem in page.xpath('//h2'):
      role, name_post = person_header_elem.text.split(' - ')
      try:
        name, caps_post = re.match(r'(.+) \((.+)\)', name_post).groups()
        post = caps_post.title()
      except AttributeError:
        name = name_post
        post = "Clarington"
      email = person_header_elem.xpath(
          'string(./following-sibling::a[1]/@href)')[len('mailto:'):]
      photo_url = person_header_elem.xpath(
          'string(./following-sibling::img[1]/@src)')
      p = Legislator(name=name, post_id=post, role=role, image=photo_url)
      p.add_source(COUNCIL_PAGE)
      p.add_contact('email', email, None)
      yield p
