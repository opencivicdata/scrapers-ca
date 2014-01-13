from pupa.scrape import Scraper, Legislator

from utils import lxmlize

import re

COUNCIL_PAGE = 'http://www.ville.pointe-claire.qc.ca/en/city-hall-administration/your-council/municipal-council.html'


class PointeClairePersonScraper(Scraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)

    mayor = page.xpath('.//div[@class="item-page clearfix"]//table[1]//p')[1]
    name = mayor.xpath('.//strong/text()')[0]

    p = Legislator(name=name, post_id='pointe-claire')
    p.add_source(COUNCIL_PAGE)
    p.role = 'Mayor'

    phone = re.findall(r'[0-9]{3} [0-9]{3}-[0-9]{4}', mayor.text_content())[0].replace(' ', '-')
    email = mayor.xpath('.//a/@href')[0]
    p.add_contact('voice', phone, 'legislature')
    p.add_contact('email', email, None)
    yield p

    rows = page.xpath('//tr')
    for i, row in enumerate(rows):
      if i % 2 == 0:
        continue
      councillors = row.xpath('./td')
      for j, councillor in enumerate(councillors):
        name = councillor.text_content()
        district = rows[i + 1].xpath('.//td//a[contains(@href, "maps")]/text()')[j] + ', ' + rows[i + 1].xpath('.//td/p[1]/text()')[j]

        p = Legislator(name=name, post_id=district)
        p.add_source(COUNCIL_PAGE)
        p.role = 'Councillor'
        p.image = councillor.xpath('.//img/@src')[0]

        phone = re.findall(r'[0-9]{3} [0-9]{3}-[0-9]{4}', rows[i + 1].xpath('.//td')[j].text_content())[0].replace(' ', '-')
        email = rows[i + 1].xpath('.//td')[j].xpath('.//a/@href')[1].replace('mailto:', '')

        p.add_contact('voice', phone, 'legislature')
        p.add_contact('email', email, None)

        yield p
