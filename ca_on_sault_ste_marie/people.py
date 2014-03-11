# coding: utf-8
from pupa.scrape import Scraper

from utils import lxmlize, CanadianLegislator as Legislator

from urlparse import urljoin

import re

COUNCIL_PAGE = 'http://www.city.sault-ste-marie.on.ca/Open_Page.aspx?ID=174&deptid=1'


class SaultSteMariePersonScraper(Scraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)
    table_data = page.xpath('//div[@id="litcontentDiv"]//tr')
    council_data = table_data[2:-1]

    mayor_row = table_data[0]
    
    photo_url_rel = mayor_row.xpath('string(.//img/@src)')
    photo_url = urljoin(COUNCIL_PAGE, photo_url_rel)
    contact_node = mayor_row.xpath('./td')[1]
    name = contact_node.xpath('string(.//strong)')
    email = contact_node.xpath('string(.//a[2])')

    p = Legislator(name=name, post_id='Sault Ste. Marie', role='Mayor')
    p.add_source(COUNCIL_PAGE)
    p.add_contact('email', email, None)
    p.image = photo_url
    yield p

    #alternate between a row represneting a ward name and councilors
    for ward_row, data_row in zip(*[iter(council_data)]*2):
      district = ward_row.xpath('string(.//text()[contains(., "Ward")])')
      for councillor_node in data_row.xpath('./td'):
        name = councillor_node.xpath('string(.//strong)')
        email = councillor_node.xpath('string(.//a)')
        photo_url_rel = councillor_node.xpath('string(.//img/@src)')
        photo_url = urljoin(COUNCIL_PAGE, photo_url_rel)
        # address and phone are brittle, inconsistent

        p = Legislator(name=name, post_id=district, role='Councillor')
        p.add_source(COUNCIL_PAGE)
        p.add_contact('email', email, None)
        p.image = photo_url

        yield p

