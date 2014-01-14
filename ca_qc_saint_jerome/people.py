from pupa.scrape import Scraper, Legislator

from utils import lxmlize

import re

COUNCIL_PAGE = 'http://www.ville.saint-jerome.qc.ca/pages/aSavoir/conseilMunicipal.aspx'


class SaintJeromePersonScraper(Scraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)

    councillors = page.xpath('//table[1]/tbody//tr')[6:]
    for councillor in councillors:
      image = councillor.xpath('.//img/@src')
      councillor = councillor.text_content().strip()

      name = councillor.split(',')[0]

      if 'district' in name:
        continue
      district = re.findall(ur'no\xa0([0-9]{1,2})', councillor)
      if not district:
        district = re.findall(ur'no ([0-9]{1,2})', councillor)

      # if theres still no district, it must be the mayor
      if not district:
        district = 'sainte-jerome'
        role = 'Mayor'
      else:
        district = district[0]
        role = 'Councillor'

      phone = re.findall(r'[0-9]{3} [0-9]{3}-[0-9]{4}', councillor)[0].replace(' ', '-')

      p = Legislator(name=name, post_id=district, role=role)
      p.add_source(COUNCIL_PAGE)
      p.image = image[0]
      p.add_contact('voice', phone, 'legislature')
      yield p
