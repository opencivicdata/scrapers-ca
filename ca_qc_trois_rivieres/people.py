# coding: utf-8
from pupa.scrape import Scraper

from utils import lxmlize, CanadianLegislator as Legislator
from urlparse import urljoin

import requests
import re

COUNCIL_PAGE = 'http://laville.v3r.net/portail/index.aspx?sect=0&module=5&module2=1&MenuID=150&CPage=1'


class TroisRivieresPersonScraper(Scraper):

  def get_people(self):
    resp = requests.get(COUNCIL_PAGE)
    # page rendering through JS on the client
    page_re = re.compile(r'createItemNiv3.+"District (.+?)".+(index.+)\\"')
    for district, url_rel in page_re.findall(resp.text):
        if district.startswith('de '):
            district = district[len('de '):]

        url = urljoin(COUNCIL_PAGE, url_rel)
        page = lxmlize(url)
        name = page.xpath('string(//h2)')
        email = page.xpath(
            'string(//a/@href[contains(., "mailto:")])')[len('mailto:'):]
        photo_url = page.xpath('string(//img/@src[contains(., "Conseiller")])')
        p = Legislator(name=name, post_id=district, role='Conseiller',
                       image=photo_url)
        p.add_source(url)
        p.add_contact('email', email, None)
        yield p
