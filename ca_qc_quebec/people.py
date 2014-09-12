# coding: utf8
from pupa.scrape import Scraper

from utils import lxmlize, CanadianLegislator as Legislator

import re

COUNCIL_PAGE = 'http://www.ville.quebec.qc.ca/apropos/vie_democratique/elus/conseil_municipal/membres.aspx'


class QuebecPersonScraper(Scraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)

    councillors = page.xpath('//div[contains(@class, "ligne")]')
    for councillor in councillors:

      name = ' '.join(councillor.xpath('.//h3')[0].text_content().strip().split(', ')[::-1])
      if 'vacant' in name:
        continue
      district = councillor.xpath('./preceding-sibling::h2/text()')[-1]
      if 'Mairie' in district:
        district = u'Québec'
        role = 'Maire'
      else:
        text = councillor.xpath('./a[@target="_blank"]/text()')
        district = re.search(u'\ADistrict électoral (?:de|du|des) (.+) - ?\d+\Z', text[0].strip(), flags=re.U).group(1)
        role = 'Conseiller'

      if district == 'Monts':
        district = 'Les Monts'
      elif district == 'Plateau':
        district = 'Le Plateau'
      else:
        district = re.sub(u'–', u'—', district)  # n-dash, m-dash
        district = re.sub('\Ala ', 'La ', district)

      p = Legislator(name=name, post_id=district, role=role)
      p.add_source(COUNCIL_PAGE)
      p.image = councillor.xpath('./p/img/@src')[0]

      phone = re.findall(r'T.l\. : ([0-9]{3} [0-9]{3}-[0-9]{4})(,.*([0-9]{4}))?', councillor.text_content())[0]
      if phone[-1]:
        phone = phone[0].replace(' ', '-') + ' x' + phone[-1]
      else:
        phone = phone[0].replace(' ', '-')
      p.add_contact('voice', phone, 'legislature')
      yield p
