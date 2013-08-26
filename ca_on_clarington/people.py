from pupa.scrape import Scraper, Legislator

from utils import lxmlize, CanadianScraper

import re

COUNCIL_PAGE = 'http://www.clarington.net/htdocs/council_bios.html'


class ClaringtonPersonScraper(CanadianScraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)
    organization = self.get_organization()
    yield organization

    councillors = page.xpath('//*[@class="subtitle"]')
    emails = page.xpath('.//a[contains(@href, "mailto:")]')
    for councillor in councillors:
      name = re.findall(r'(([A-Z]+ ?){2,})', councillor.text_content())[0][0].lower()
      district = re.findall(r'\((.*)\)?', councillor.text_content())
      if not district:
        district = 'clarington'
        role = 'mayor'
      else:
        district = district[0].replace(")", '')
        role = 'councillor'
      email = emails.pop(0).attrib['href'].split(':')[1]

      image = councillor.xpath('.//following-sibling::img/@src')
      if image:
        image = image[0]
      else:
        image = councillor.xpath('.//parent::*/following-sibling::*//@src')[0]



      p = Legislator(name=name, post_id=district)
      p.add_source(COUNCIL_PAGE)
      p.add_membership(organization, role=role)
      p.add_contact('email', email, None)
      p.image = image
      yield p
