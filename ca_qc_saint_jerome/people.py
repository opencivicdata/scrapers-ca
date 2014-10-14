# coding: utf-8
from __future__ import unicode_literals
from pupa.scrape import Scraper

import re

from utils import lxmlize, CanadianPerson as Person

COUNCIL_PAGE = 'http://www.ville.saint-jerome.qc.ca/pages/aSavoir/conseilMunicipal.aspx'


class SaintJeromePersonScraper(Scraper):

  def scrape(self):
    page = lxmlize(COUNCIL_PAGE)

    councillor_trs = [tr for tr in page.xpath('//table//tr[1]') if len(tr) == 2][:-1]
    for councillor_tr in councillor_trs:
      desc = [text.strip() for text in councillor_tr.xpath('.//text()[normalize-space()]') if text.strip()]

      if len(desc) == 3:
        role = 'Maire'
        district = 'Saint-Jérôme'
      else:
        role = 'Conseiller'
        district = desc[0].replace('numéro ', '')

      name = desc[-3]
      phone = desc[-2]
      email = desc[-1]

      image = councillor_tr.xpath('string(.//img/@src)')[0]

      p = Person(name=name, post_id=district, role=role)
      p.add_source(COUNCIL_PAGE)
      p.image = image
      p.add_contact('voice', phone, 'legislature')
      p.add_contact('email', email, None)
      yield p
