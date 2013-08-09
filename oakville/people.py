from pupa.scrape import Scraper, Legislator
from larvae.person import Person
from larvae.organization import Organization

from utils import lxmlize

import re

COUNCIL_PAGE = 'http://www.oakville.ca/townhall/council.html'

class OakvillePersonScraper(Scraper):
  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)

    councillors = page.xpath('//div[contains(@class,"fourcol")]')
    # councillors.append(page.xpath('//div[@class = "fourcol multicollast"]')[1::-1])
    for councillor in councillors:
      if len(councillor.xpath('.//h2')) < 3:
         name = councillor.xpath('.//h2')[1].text_content()
         p = Legislator(name=name, post_id="Oakville")
         url = councillor.xpath('.//a')[0].attrib['href']
         self.scrape_mayor(url,p)
         yield p
      else:
        name = councillor.xpath('.//h2')[2].text_content()
        district = councillor.xpath('.//h2')[0].text_content()

        p = Legislator(name=name, post_id=district)
        url = councillor.xpath('.//a')[0].attrib['href']
        self.scrape_councillor(url, p)
        yield p
    
  def scrape_mayor(self, url, mayor):
    page = lxmlize(url)
    mayor.add_source(COUNCIL_PAGE)
    mayor.add_source(url)

    ## gather contact details
    info = page.xpath('//div[@class="fourcol multicol"]//p')[0]
    phone = re.findall(r'tel: (\S*)', info.text_content())[0]
    fax = re.findall(r'fax: (\S*)', info.text_content())[0]
    email = info.xpath('.//a[contains(@href, "mailto:")]')[0].text_content()

    ## save contact details to object
    mayor.add_contact('phone', phone, None)
    mayor.add_contact('fax', fax, None)
    mayor.add_contact('email', email, None)

    ## extra sites
    twitter = info.xpath('.//a[contains(@href, "twitter")]')[0].attrib['href']
    facebook = info.xpath('.//a[contains(@href, "facebook")]')[0].attrib['href']
    mayor.add_link(twitter, 'twitter')
    mayor.add_link(facebook, 'facebook')


  def scrape_councillor(self, url, councillor):
    page = lxmlize(url)
    councillor.add_source(COUNCIL_PAGE)
    councillor.add_source(url)

    info = page.xpath('//div[@class = "fourcol multicollast"]//p')[1].text_content()
    
    ## extract contact information
    address = re.findall(r'([0-9].*([A-Z][0-9][A-Z] [0-9][A-Z][0-9]))', info, flags=re.DOTALL)
    if address:
      address = re.sub(r'\W{2,}',' ' , str(address[0])).decode()
      address = address.replace("u'",'').replace(' n ',', ').replace("(",'')

    phone = re.findall(r'tel: (\S*)|phone: (\S*)', info)
    if not phone:
      phone = re.findall(r'([0-9]{3}[- ][0-9]{3}[- ][0-9]{4})',info)
    if 'tuple' in str(type(phone[0])):
      phone = next(x for x in phone[0] if x != '')
    else:
      phone = phone[0]
    fax = re.findall(r'fax: (\S*) ',info)
    emails = page.xpath('//div[@class = "fourcol multicollast"]//a[contains(@href, "mailto:")]')
    ## save contact info to councillor object
    if address:
      councillor.add_contact('address', address, None)
    councillor.add_contact('phone', str(phone), None)
    if fax:
      councillor.add_contact('fax', str(fax[0]), None)
    councillor.add_contact('email', emails[0].text_content(), councillor.name)
    councillor.add_contact('email', emails[1].text_content(), 'district')

    ## extra links
    if "Twitter" in info:
      link = page.xpath('//div[@class = "fourcol multicollast"]//a[contains(@href, "twitter")]')[0].attrib['href']
      councillor.add_link(link,'twitter')
    if "Facebook" in info:
      link = page.xpath('//div[@class = "fourcol multicollast"]//a[contains(@href, "facebook")]')[0].attrib['href']
      councillor.add_link(link,'facebook')
    if "LinkedIn" in info:
      link = page.xpath('//div[@class = "fourcol multicollast"]//a[contains(@href, "linkedin")]')[0].attrib['href']
      councillor.add_link(link,'linkedin')

