from pupa.scrape import Scraper, Legislator

from utils import lxmlize

import re

COUNCIL_PAGE = 'http://www.gatineau.ca/page.asp?p=la_ville/conseil_municipal'


class GatineauPersonScraper(Scraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)

    councillors = page.xpath('//div[@id = "submenu_content"]//li')
    for councillor in councillors:
      name = councillor.text_content()
      if "maire" in name:
        yield self.scrape_mayor(councillor.xpath('.//a')[0].attrib['href'])
        continue
      url = councillor.xpath('.//a')[0].attrib['href']
      page = lxmlize(url)
      content = page.xpath('//div[@id="pagecontent"]')[0]
      district = content.xpath('.//h2')
      if not district:
        continue
      district = district[0].text_content()

      phone = re.findall(r'([0-9]{3} [0-9]{3}-[0-9]{4})', content.text_content())[0].replace(' ', '-')
      email = content.xpath('//a[contains(@href, "mailto:")]')[0].text_content()

      p = Legislator(name=name, post_id=district, role='Councillor')
      p.add_source(COUNCIL_PAGE)
      p.add_source(url)
      p.add_contact('voice', phone, 'legislature')
      p.add_contact('email', email, None)
      p.image = content.xpath('//table//td/img/@src')[0]

      if "site" in content.text_content():
        p.add_link(content.xpath('.//a')[1].attrib['href'], None)

      yield p

  def scrape_mayor(self, url):
    page = lxmlize(url)
    contact_url = page.xpath('//a[contains(text(), "Communiquez")]')[0].attrib['href']
    page = lxmlize(contact_url)

    content = page.xpath('//div[@id="pagecontent"]')[0]
    name = content.xpath('.//h2')[0].text_content()
    phone = re.findall(r'([0-9]{3} [0-9]{3}-[0-9]{4})', content.text_content())[0].replace(' ', '-')
    email = content.xpath('.//a[contains(@href, "mailto:")]')[0].text_content()

    p = Legislator(name=name, post_id='Gatineau', role='Mayor')
    p.add_source(COUNCIL_PAGE)
    p.add_source(contact_url)
    p.add_contact('voice', phone, 'legislature')
    p.add_contact('email', email, None)

    return p
