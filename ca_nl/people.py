# coding: utf-8
from pupa.scrape import Scraper

from utils import lxmlize, CanadianLegislator as Legislator

import re

COUNCIL_PAGE = 'http://www.assembly.nl.ca/members/cms/membersdirectlines.htm'
PARTY_PAGE = 'http://www.assembly.nl.ca/members/cms/membersparty.htm'


class NewfoundlandAndLabradorPersonScraper(Scraper):

  def get_people(self):
    member_parties = dict(process_parties(lxmlize(PARTY_PAGE)))

    page = lxmlize(COUNCIL_PAGE)
    for row in page.xpath('//table[not(@id="footer")]/tr')[1:]:
      name, district, _, email = [
          cell.xpath('string(.)').replace(u'\xa0', u' ') for cell in row]
      phone = row[2].xpath('string(text()[1])')
      try:
        photo_page_url = row[0].xpath('./a/@href')[0]
      except IndexError:
        continue # there is a vacant district
      photo_page = lxmlize(photo_page_url)
      photo_url = photo_page.xpath('string(//table//img/@src)')
      district = district.replace(' - ', u'—')  # m-dash
      party = member_parties[name]
      p = Legislator(name=name, post_id=district, role='MHA', 
          party=party, image=photo_url)
      p.add_source(COUNCIL_PAGE)
      p.add_source(photo_page_url)
      p.add_contact('email', email, None)
      # TODO: either fix phone regex or tweak phone value
      p.add_contact('voice', phone, 'legislature')
      yield p

def process_parties(partypage):
  # return generator of (name, party) tuples for MHAs
  for elem in partypage.xpath('//h3/u'):
    party = elem.text
    members = elem.xpath('./ancestor::tr/following-sibling::tr/td/a')
    member_names = [elem.text.replace(u'\xa0', u' ') for elem in members]
    for name in member_names:
      yield (name, party)
