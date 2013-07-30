from pupa.scrape import Scraper, Legislator
from larvae.person import Person
from larvae.organization import Organization

from .utils import lxmlize

import re

COUNCIL_PAGE = 'http://www.cambridge.ca/cs_mayor/wards_councillors.php?cpid=51&sid=57'

class CambridgePersonScraper(Scraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)

    councillors = page.xpath('//div[@id="news"]//p')
    for councillor in councillors:
      district = councillor.xpath('./b')[0].text_content()
      district = re.findall(u'W|R.*',district)[0]
      if 'Regional' in district:
        district = 'cambridge'
      name = councillor.xpath('.//a')[0].text_content()

      url = councillor.xpath('.//a')[0].attrib['href']
      page = lxmlize(url)

      address = page.xpath('//*[contains(text(),"Address")]/ancestor::td')[-1].text_content().split(':')[-1]
      phone = page.xpath('//*[contains(text(),"Tel")]/ancestor::td')[-1].text_content().split(':')[-1]
      if page.xpath('//*[contains(text(),"Fax")]'):
        fax = page.xpath('//*[contains(text(),"Fax")]/ancestor::td')[-1].text_content().split(':')[-1]
      email = page.xpath('//a[contains(@href,"mailto:")]')[0].text_content()
      
      p = Legislator(name=name, district=district)
      p.add_source(COUNCIL_PAGE)
      p.add_source(url)
      p.add_contact('address', address, None)
      p.add_contact('phone', phone, None)
      p.add_contact('fax', fax, None)
      p.add_contact('email', email, None)
      yield p
