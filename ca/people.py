# coding: utf-8
from pupa.scrape import Scraper

from utils import lxmlize, CanadianLegislator as Legislator

import re

COUNCIL_PAGE = 'http://www.parl.gc.ca/Parliamentarians/en/members?view=ListAll'


class CanadaPersonScraper(Scraper):
  """
  The CSV at http://www.parl.gc.ca/Parliamentarians/en/members/export?output=CSV
  accessible from http://www.parl.gc.ca/Parliamentarians/en/members has no
  contact information or photo URLs.
  """

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)
    rows = page.xpath('//div[@class="main-content"]//tr')[1:]
    for row in rows:
      name_cell = row.xpath('./td[1]')[0]
      last_name = name_cell.xpath('string(.//span[1])')
      first_name = name_cell.xpath('string(.//span[2])')
      name = '%s %s' % (first_name, last_name)
      constituency = row.xpath('string(./td[2])')
      province = row.xpath('string(./td[3])')
      party = row.xpath('string(./td[4])')

      url = name_cell.xpath('string(.//a/@href)')
      mp_page = lxmlize(url)
      email = mp_page.xpath('string(//span[@class="caucus"]/'
                            'a[contains(., "@")])')
      photo = mp_page.xpath('string(//div[@class="profile overview header"]//'
                            'img/@src)')

      m = Legislator(name=name, post_id=constituency, role='MP', chamber='lower', party=party)
      m.add_source(COUNCIL_PAGE)
      m.add_source(url)
      # @see http://www.parl.gc.ca/Parliamentarians/en/members/David-Yurdiga%2886260%29
      if email:
        m.add_contact('email', email, None)
      m.image = photo

      if mp_page.xpath('string(//span[@class="province"][0])') == u'Québec':
        m.add_contact('address', 'Chambre des communes\nOttawa ON  K1A 0A6', 'legislature')
      else:
        m.add_contact('address', 'House of Commons\nOttawa ON  K1A 0A6', 'legislature')
      voice = mp_page.xpath('string(//div[@class="hilloffice"]//span[contains(text(), "Telephone:")])')
      if voice:
        m.add_contact('voice', voice.replace('Telephone: ', ''), 'legislature')
      fax = mp_page.xpath('string(//div[@class="hilloffice"]//span[contains(text(), "Fax:")])').replace('Fax: ', '')
      if fax:
        m.add_contact('fax', fax, 'legislature')

      for li in mp_page.xpath('//div[@class="constituencyoffices"]//li'):
        spans = li.xpath('./span[not(@class="spacer")]')
        m.add_contact('address', '\n'.join([
          spans[0].text_content(), # address line 1
          spans[1].text_content(), # address line 2
          spans[2].text_content(), # city, region
          spans[3].text_content(), # postal code
        ]), 'constituency')
        voice = li.xpath('string(./span[contains(text(), "Telephone:")])').replace('Telephone: ', '')
        if voice:
          m.add_contact('voice', voice, 'constituency')
        fax = li.xpath('string(./span[contains(text(), "Fax:")])').replace('Fax: ', '')
        if fax:
          m.add_contact('fax', fax, 'constituency')

      yield m
