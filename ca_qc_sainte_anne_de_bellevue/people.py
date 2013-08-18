from pupa.scrape import Scraper, Legislator

from utils import lxmlize

import re

COUNCIL_PAGE = 'http://www.ville.sainte-anne-de-bellevue.qc.ca/Democratie.aspx'

class SainteAnneDeBellevuePersonScraper(Scraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)
    councillors = page.xpath('//div[@id="content"]//td')
    for councillor in councillors:
      if not councillor.text_content().strip():
        continue
      if 'Maire' in councillor.text_content():
        name = councillor.xpath('.//a')[0].text_content()
        district = 'Sainte-Anne-de-Bellevue'
      else:
        name = re.findall(r'(?<=[0-9]).*', councillor.text_content(), flags=re.DOTALL)[0].strip()
        district = re.findall(r'(.*[0-9])', councillor.text_content())[0].replace('Conseiller','')

      p = Legislator(name=name, post_id=district)
      p.add_source(COUNCIL_PAGE)

      email = councillor.xpath('.//a')
      if email:
        email = email[0].attrib['href'].replace('mailto:', '')
        p.add_contact('email', email, None)
      yield p