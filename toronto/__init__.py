from pupa.scrape import Jurisdiction, Scraper, Legislator
from larvae.organization import Organization
from larvae.person import Person
from scrapelib import urlopen

import lxml.html
import re

COUNCIL_PAGE = 'http://app.toronto.ca/im/council/councillors.jsp'

class Toronto(Jurisdiction):
  jurisdiction_id = 'ca-on-to'

  def get_metadata(self):
    return {'name': 'Toronto',
            'legislature_name': 'Toronto City Council',
            'legislature_url': 'http://www.toronto.ca/city_hall/index.htm',
            'terms': [{'name': '2010-2014', 'sessions': ['2010-2014'],
                       'start_year': 2010, 'end_year': 2014
            }],
            'provides': ['people'],
            'parties': [],
            'session_details': {'2010-2014': {'_scraped_name': '2010-2014'}},
            'feature_flags': [],
            '_ignored_scraped_sessions': ['2006-2010']

    }
  def get_scraper(self, term, session, scraper_type):
    if scraper_type == 'person':
        return TorontoPersonScraper

  def scrape_session_list(self): 
    page = self.lxmlize('http://app.toronto.ca/tmmis/findAgendaItem.do?function=doPrepare')
    return page.xpath("//select[@id='termId']//option[position()>1]/text()")

  def lxmlize(self, url, encoding = 'utf-8'):
    entry = urlopen(url).encode(encoding)
    return lxml.html.fromstring(entry)

class TorontoPersonScraper(Scraper):
  def lxmlize(self, url, encoding = 'utf-8'):
    entry = self.urlopen(url).encode(encoding)
    page = lxml.html.fromstring(entry)
    page.make_links_absolute(url)
    return page


  def get_people(self):
    yield self.toronto_scrape_people
  def toronto_scrape_people(self):
    page = self.lxmlize(COUNCIL_PAGE) 
    table = page.xpath('//table[3]//td/font/a')
    for index, element in enumerate(table):
      url = element.attrib['href']
      if index == 0:
        p = self.scrape_mayor()
        yield p
      else:
        p = self.scrape_councilor(url)
        yield p
  def scrape_councilor(self, url):
    page = self.lxmlize(url)
    info = page.xpath("//div[@class='main']")[0]
    name = info.xpath("//h3")[1].text_content().replace('Councillor','').strip()
    district = info.xpath("//p")[0].text_content()
    p = Legislator(name=name, district=district)
    
    info = info.xpath("//div[@class='last']")[0]

    # add links
    p.add_source(url)
    p.add_source(COUNCIL_PAGE)
     
    if "website:" in info.text_content():
      p.add_link(info.xpath('.//a')[1].attrib['href'], 'homepage')

    if "Facebook" in info.text_content():
      p.add_link(info.xpath('//a[contains(@href, "facebook.com")]')[0].attrib['href'],'facebook')
   
    if "Twitter" in info.text_content():
      p.add_link(info.xpath('//a[contains(@href,"twitter.com")]')[0].attrib['href'],'twitter') 
    
    # add contact info
    p.add_contact('email', info.xpath('.//a')[0].text_content(),'')
   #//*[@id="content"]/div/div[1]/div[2]/p[1]
    contacts = info.xpath('//div/p[text()[contains(.,"Phone:")]]')
    for contact in contacts:
      note = contact.xpath('.//strong')[0].text_content()
      contact = contact.xpath('br/following-sibling::node()')
      if len(contact) > 8 : continue
      if len(contact) >= 4:
        address = (contact[0]+", "+contact[2]).strip()
        p.add_contact('address',address,note)
        if "Phone: " in contact[4]: 
          phone = contact[4].replace("Phone: ",'').strip()
          p.add_contact('phone',phone,note)
        if len(contact) > 5 and "Fax:" in contact[6]: 
          fax = contact[6].replace("Fax: ",'').strip()
          p.add_contact('fax',fax,note) 
      else: 
        phone = contact[0].strip()
        p.add_contact('phone',phone,note)
        fax = contact[2].strip()
        p.add_contact('fax',fax,note)


    

  def scrape_mayor(self):
    url = 'http://www1.toronto.ca/wps/portal/contentonly?vgnextoid=e53332d0b6d1e310VgnVCM10000071d60f89RCRD&vgnextfmt=default'
    page = self.lxmlize(url)
    name = page.xpath("//div[@class='detail']//h1/text()")[0].replace("Toronto Mayor","").strip()
    p = Legislator(name,"Toronto")
    
    p.add_source(COUNCIL_PAGE)
    p.add_source(url)

    url = page.xpath('//a[contains(text(),"Contact the Mayor")]')[0].attrib['href']
    p.add_source(url)
    page = self.lxmlize(url)

    info = page.xpath('//div[@class="detail"]')[0]
    address = (', ').join(info.xpath('.//p/text()')[0:6]).replace(",,",",")
    phone = info.xpath('.//p[3]/text()')[0]
    
    p.add_contact('address',address,'Mailing')
    p.add_contact('phone',phone,'')



#t = Toronto()
#s = TorontoPersonScraper(t,'m','/Users/alexio/Desktop',)
#s.toronto_scrape_people()
#s.toronto_scrape_people()