from pupa.scrape import Scraper

from utils import lxmlize, CanadianLegislator as Legislator

import re

COUNCIL_PAGE = 'http://www.wellesley.ca/council/councillors/?q=council/councillors'

def post_number(name):
    return {
      'Ward One': 'Ward 1',
      'Ward Two': 'Ward 2',
      'Ward Three': 'Ward 3',
      'Ward Four': 'Ward 4'
    }[name]

class WellesleyPersonScraper(Scraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)

    councillors = page.xpath('//div[@class="img_four"][1]/div[1]')
    councillors = councillors + page.xpath('//div[@class="img_four"][2]/div')
    for councillor_elem in councillors:
      name, position = councillor_elem.xpath('string(./p/strong)').split(',')
      position = position.strip()
      if ' ' in position:
        position, post_id = position.split(' ', 1)
        post_id = post_number(post_id)
      else:
        post_id = 'Wellesley'
      addr = '\n'.join(addr_str.strip() for addr_str in 
                      councillor_elem.xpath('./p/text()')).strip()
      phone = councillor_elem.xpath('string(.//a[starts-with(@href, "tel:")])')
      email = councillor_elem.xpath(
          'string(.//a[starts-with(@href, "mailto:")])')
      image = councillor_elem.xpath('string(.//img[1]/@src)')
      p = Legislator(name=name, post_id=post_id, role=position, image=image)
      p.add_source(COUNCIL_PAGE)
      p.add_contact('address', addr, 'legislature')
      p.add_contact('voice', phone, 'legislature')
      p.add_contact('email', email, None)
      yield p

