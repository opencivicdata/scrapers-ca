from pupa.scrape import Scraper, Legislator

from utils import lxmlize

import re

COUNCIL_PAGE = 'http://www.clarington.net/htdocs/council_bios.html'

class ClaringtonPersonScraper(Scraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)

    councillors = page.xpath('//*[@class="subtitle"]')
    emails = page.xpath('.//a[contains(@href, "mailto:")]')
    for councillor in councillors:
      name = re.findall(r'(([A-Z]+ ?){2,})', councillor.text_content())[0][0].lower()
      district = re.findall(r'\((.*)\)?', councillor.text_content())
      if not district:
        district = 'clarington'
      else:
        district = district[0].replace(")", '')
      email = emails.pop(0).attrib['href'].split(':')[1]

      p = Legislator(name=name, post_id=district)
      p.add_source(COUNCIL_PAGE)
      p.add_contact('email', email, None)
      yield p