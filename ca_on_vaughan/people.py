from __future__ import unicode_literals
from pupa.scrape import Scraper

import re

from utils import lxmlize, CanadianPerson as Person

COUNCIL_PAGE = 'http://www.vaughan.ca/council/Pages/default.aspx'


class VaughanPersonScraper(Scraper):

  def scrape(self):
    page = lxmlize(COUNCIL_PAGE)

    councillors = page.xpath('//div[@class="PL_Column1"]//ul[@class="dfwp-list"][1]/li/div/div/a')
    for councillor in councillors:
      url = councillor.attrib['href']
      page = lxmlize(url)

      title = page.xpath('//div[@class="PL_Title"]')[0].text_content()
      if "Councillor" in title:
        district, name = re.split(r'Councillor', title)
        role = 'Councillor'
        if "Regional" in district:
          district = "Vaughan"
          role = 'Regional Councillor'
      else:
        name = re.split(r'Mayor', title)[-1]
        district = 'Vaughan'
        role = 'Mayor'
      name = name.strip()
      if councillor == councillors[0]:
        contact_info = page.xpath('//div[@id="WebPartWPQ2"]')[0]
      else:
        contact_info = page.xpath('//div[@id="WebPartWPQ3"]')[0]

      phone = re.findall(r'[0-9]{3}-[0-9]{3}-[0-9]{4} ext. [0-9]{4}', contact_info.text_content())[0].replace('ext. ', 'x')
      fax = re.findall(r'[0-9]{3}-[0-9]{3}-[0-9]{4}', contact_info.text_content())[1]
      email = contact_info.xpath('.//a[contains(@href, "mailto:")]')[0].text_content()

      p = Person(name=name, district=district.strip(), role=role)
      p.add_source(COUNCIL_PAGE)
      p.add_source(url)
      p.add_contact('voice', phone, 'legislature')
      p.add_contact('fax', fax, 'legislature')
      p.add_contact('email', email, None)

      image = page.xpath('//img[contains(@alt, "Councillor")]/@src')
      if image:
        p.image = image[0]

      sites = page.xpath('//div[@id="WebPartWPQ5"]')[0]

      if page.xpath('.//a[contains(@href,"facebook")]'):
        p.add_link(page.xpath('.//a[contains(@href,"facebook")]')[0].attrib['href'], None)
      if page.xpath('.//a[contains(@href,"twitter")]'):
        p.add_link(page.xpath('.//a[contains(@href,"twitter")]')[0].attrib['href'], None)
      if page.xpath('.//a[contains(@href,"youtube")]'):
        p.add_link(page.xpath('.//a[contains(@href, "youtube")]')[0].attrib['href'], None)
      yield p
