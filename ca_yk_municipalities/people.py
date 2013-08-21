from pupa.scrape import Scraper, Legislator

from utils import lxmlize

import re
import urllib2
import os

COUNCIL_PAGE = 'http://www.community.gov.yk.ca/pdf/loc_govdir.pdf'


class YukonPersonScraper(Scraper):

  def get_people(self):
    response = urllib2.urlopen(COUNCIL_PAGE).read()
    pdf = open('yk.pdf', 'w')
    pdf.write(response)
    pdf.close()

    os.system('pdftotext -layout yk.pdf')
    txt = open('yk.txt', 'r')
    data = txt.read()
    data = re.split(r'\n\s*\n', data)
    for municipality in data:
      
      if not 'Councillors' in municipality:
        continue  
      lines = municipality.split('\n')
      if 'Page' in lines[0]:
        lines.pop(0)
        if not lines[0].strip():
          lines.pop(0)
      col1end = re.search(r'\s{2,}(\w)', lines[0].strip()).end()
      col2end = re.search(r':\s{2,}(\w)', lines[0].strip()).end()
      

      if 'Council' in lines[1]:
        address = lines[2][:col1end-1].strip() + ' ' + lines[3][:col1end-1].strip()
        district = lines[0][:col1end-1].strip() + ' ' + lines[1][:col1end-1].strip()
      else:
        address = lines[1][:col1end-1].strip() + ' ' + lines[2][:col1end-1].strip()
        district = lines[0][:col1end-1].strip()
      phone = re.findall(r'(?<=Phone: )\(?(\d{3}[\)-] ?\d{3}-\d{4})', municipality)[0].replace(') ','-')
      email = re.findall(r'(?<=E-mail:) (\S*)', municipality )[0]
      fax = None
      if 'Fax' in municipality:
        fax = re.findall(r'(?<=Fax: )\(?(\d{3}[\)-] ?\d{3}-\d{4})', municipality)[0].replace(') ','-')
      website = None
      if 'Website' in municipality:
        website = re.findall(r'http\S*', municipality)[0]
      
      councillor_or_mayor = False      
      for line in lines:
        if 'Mayor:' in line or 'Councillors' in line:
          councillor_or_mayor = True
          continue
        if councillor_or_mayor:
          councillor = line[col1end-1:col2end-1].strip()
          if not councillor:
            continue
          p = Legislator(name=councillor,post_id=district)
          p.add_source(COUNCIL_PAGE)
          p.add_contact('address', address, None)
          p.add_contact('phone', phone, None)
          p.add_contact('email', email, None)
          if fax:
            p.add_contact('fax', fax, None)
          if website:
            p.add_link(website, 'municipal website')
          yield p

    



    txt.close()
    os.system('rm yk.pdf')
    os.system('rm yk.txt')
