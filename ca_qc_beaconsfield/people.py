from pupa.scrape import Scraper, Legislator

from utils import lxmlize, CanadianScraper
import HTMLParser
import re

COUNCIL_PAGE = 'http://www.beaconsfield.ca/en/your-council.html'


class BeaconsfieldPersonScraper(CanadianScraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)
    organization = self.get_organization()
    yield organization

    councillors = page.xpath('//h1[@class="title"]')
    for councillor in councillors:
      if not ',' in councillor.text_content():
        continue
      name, district = councillor.text_content().split(',')
      name = name.strip()
      if 'Mayor' in district:
        p = Legislator(name=name, post_id='beaconsfield')
        p.add_source(COUNCIL_PAGE)
        p.add_membership(organization, role='mayor')
        p.image = councillor.xpath('./parent::div/parent::div/p//img/@src')[0]
        phone = councillor.xpath('.//parent::div/following-sibling::div[contains(text(), "514")]/text()')[0]
        phone = phone.split(':')[1].strip().replace(' ','-')
        p.add_contact('phone', phone, 'office')
        script = councillor.xpath('.//parent::div/following-sibling::div/script')[0].text_content()
        p.add_contact('email', get_email(script), None)
        yield p
        continue

      district = district.split('-')[1].strip()
      p = Legislator(name=name, post_id=district)
      p.add_source(COUNCIL_PAGE)
      p.add_membership(organization, role='councillor')

      p.image = councillor.xpath('./parent::div/parent::div/p//img/@src')[0]

      phone = councillor.xpath('.//parent::div/following-sibling::p[contains(text(), "514")]/text()')
      if phone:
        phone = phone[0]
        phone = phone.split(':')[1].strip().replace(' ','-')
        p.add_contact('phone', phone, 'office')
      script = councillor.xpath('.//parent::div/following-sibling::p/script')[0].text_content()
      p.add_contact('email', get_email(script), None)
      yield p

def get_email(script):
  var = re.findall(r'var addy\d{4,5} = \'(.*)\'', script)[0].replace('\' + \'','').replace('\'','')
  ext = re.findall(r'addy\d{4,5} = addy\d{4,5} \+ \'(.*);', script)[0].replace('\' + \'','').replace('\'','')
  h = HTMLParser.HTMLParser()
  email = h.unescape(var+ext)
  return email