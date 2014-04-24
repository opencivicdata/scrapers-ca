from __future__ import unicode_literals

from pupa.scrape import Scraper

from utils import lxmlize, CanadianLegislator as Legislator

import re

COUNCIL_PAGE = 'http://www.belleville.ca/city-hall/page/city-council'


class BellevillePersonScraper(Scraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)

    mayor_name_elem = page.xpath('//div[@class="content-field"]//a[1]')[0]
    yield person_from_elem(mayor_name_elem, 'Belleville', 'Mayor')

    ward_elems = page.xpath('//h3[contains(text(), "Councillors")]')
    for ward_elem in ward_elems:
      ward = re.search(r'(Ward.+) Councillors', ward_elem.text).group(1)
      councillor_name_elems = ward_elem.xpath(
          './following-sibling::div[1]//strong')
      for name_elem in councillor_name_elems:
        yield person_from_elem(name_elem, ward, 'Councillor')


def person_from_elem(name_elem, post_id, role):
  name = name_elem.text_content()
  phone = name_elem.xpath(
      'string(./following-sibling::text()[2])').split(': ')[1]
  if not phone.startswith('613-'):
    corrected_phone = '613-' + phone
  else:
    corrected_phone = phone
  email = name_elem.xpath('string(./following-sibling::a)')
  photo_url = name_elem.xpath('string(./parent::p/preceding::img[1]/@src)')
  p = Legislator(name=name, post_id=post_id, role=role, image=photo_url)
  p.add_source(COUNCIL_PAGE)
  p.add_contact('voice', corrected_phone, 'legislature')
  p.add_contact('email', email, None)
  return p
