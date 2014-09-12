# coding: utf-8
from pupa.scrape import Scraper

from utils import lxmlize, CanadianLegislator as Legislator

import re

COUNCIL_PAGE = 'http://www.longueuil.ca/fr/conseil-ville'


class LongueuilPersonScraper(Scraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE, 'latin-1')
    person_rows = [tr for tr in page.xpath('//tr') if
                   tr.xpath('./td[2][@class="TABL1"]')]
    leader_row = person_rows[0]
    councillor_rows = person_rows[1:]
    for row in councillor_rows:
        district = row[1].text if row[1].text.strip() else 'Greenfield Park'
        name = row[2].xpath('string(./a)').title()
        detail_url = row[2].xpath('string(./a/@href)')
        detail_page = lxmlize(detail_url)
        email_url = detail_page.xpath(
            'string(//a[contains(@href, "sendto")]/@href)')
        email = re.search(r'sendto=(.+)&', email_url).group(1)
        photo_url = detail_page.xpath('string(//img[@height="200"]/@src)')
        p = Legislator(name=name, post_id=district, role='Conseiller')
        p.add_source(COUNCIL_PAGE)
        p.add_source(detail_url)
        p.image = photo_url
        p.add_contact('email', email, None)
        yield p

    mayor_td = leader_row[1]
    name, position = [string.title() for string in
                      mayor_td.text_content().split(', ')]
    mayor_url = mayor_td.xpath('string(.//a/@href)')
    mayor_page = lxmlize(mayor_url)
    photo_url = mayor_page.xpath('string(//b/img/@src)')
    email_url = detail_page.xpath(
        'string(//a[contains(@href, "sendto")]/@href)')
    email = re.search(r'sendto=(.+)&', email_url).group(1)
    p = Legislator(name=name, post_id='Longueuil', role='Maire')
    p.add_source(COUNCIL_PAGE)
    p.add_source(mayor_url)
    p.image = photo_url
    p.add_contact('email', email, None)
    yield p
