# coding: utf8
from pupa.scrape import Scraper

from utils import lxmlize, CanadianLegislator as Legislator

import re

COUNCIL_PAGE = 'http://www.ville.saint-jerome.qc.ca/pages/aSavoir/conseilMunicipal.aspx'


class SaintJeromePersonScraper(Scraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)

    councillor_trs = [tr for tr in page.xpath('//table//tr[1]') if 
            len(tr) == 2][:-1]
    for councillor_tr in councillor_trs:
      desc = [line.strip() for line in 
              councillor_tr.text_content().strip().split('\n')]
      if len(desc) == 3:
        role = 'Maire'
        district = u'Saint-Jérôme'
      else:
        role = 'Conseiller'
        district = desc[0].replace(u'numéro ', '')

      name = desc[-3]
      phone = desc[-2]
      email = desc[-1]

      image = councillor_tr.xpath('string(.//img/@src)')[0]
      
      p = Legislator(name=name, post_id=district, role=role)
      p.add_source(COUNCIL_PAGE)
      p.image = image
      p.add_contact('voice', phone, 'legislature')
      p.add_contact('email', email, None)
      yield p
