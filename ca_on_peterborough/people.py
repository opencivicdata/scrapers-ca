from pupa.scrape import Scraper, Legislator

from utils import lxmlize, CanadianScraper

import re

COUNCIL_PAGE = 'http://www.peterborough.ca/City_Hall/City_Council_2833/City_Council_Contact_Information.htm'


class PeterboroughPersonScraper(CanadianScraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)
    organization = self.get_organization()
    yield organization

    mayor_info = page.xpath('//h2[contains(text(), "MAYOR")]//following-sibling::p')[0]
    yield self.scrape_mayor(mayor_info, organization)

    wards = page.xpath('//h3')
    for ward in wards:
      district = ward.text_content()
      councillors = ward.xpath('following-sibling::p')
      for councillor in councillors:
        name = councillor.xpath('./strong')[0].text_content()

        p = Legislator(name=name, post_id=district)
        p.add_source(COUNCIL_PAGE)
        p.add_membership(organization, role='councillor')

        info = councillor.xpath('./text()')
        address = info.pop(0)
        p.add_contact('address', address, 'legislature')

        # get phone numbers
        for line in info:
          stuff = re.split(ur'(\xbb)|(\xa0)', line)
          tmp = [y for y in stuff if y and not re.match(ur'\xa0', y)]
          # print tmp
          self.get_tel_numbers(tmp, p)

        email = councillor.xpath('.//a[contains(@href, "mailto")]/@href')[0].replace('mailto:', '')

        yield p
        if councillor == councillors[1]:
          break

  def scrape_mayor(self, info, organization):
    name = info.xpath('./strong')[0].text_content()
    email = info.xpath('.//a[contains(@href, "mailto:")]')[0].text_content()

    info = info.xpath('./text()')[0:3]
    address = info[0]
    phone = re.findall(r'[0-9].*', info[1])[0].replace(u'\xa0', ' ')
    fax = re.findall(r'[0-9].*', info[2])[0]

    p = Legislator(name=name, post_id="peterborough")
    p.add_source(COUNCIL_PAGE)
    p.add_membership(organization, role='mayor')

    p.add_contact('email', email, None)
    p.add_contact('address', address, 'legislature')
    p.add_contact('voice', phone, 'legislature')
    p.add_contact('fax', fax, 'legislature')
    return p

  def get_tel_numbers(self, line, councillor):
    for i, x in enumerate(line):
      if u'\xbb' in x and not 'E-Mail' in line[i - 1]:
        contact_type = "voice" if not "Fax" in line[i - 1] else "fax"
        if 'Voice Mail' in line[i - 1]:
          number = line[i + 1] if not re.match(r'x[0-9]', line[i + 2]) else line[i + 1] + ' ' + line[i + 2]
        else:
          number = line[i + 1]
        councillor.add_contact(contact_type, number, line[i - 1].strip())
