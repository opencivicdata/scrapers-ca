# coding: utf-8
from __future__ import unicode_literals
from utils import CanadianScraper, CanadianPerson as Person

COUNCIL_PAGE = 'http://www.assnat.qc.ca/fr/deputes/index.html'


class QuebecPersonScraper(CanadianScraper):

    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)
        for row in page.xpath('//*[@id="ListeDeputes"]/tbody/tr'):
            name_comma, division = [cell.text_content() for cell in row[:2]]
            name = ' '.join(reversed(name_comma.strip().split(',')))
            party = row[2].text_content()
            email = self.get_email(row[3], error=False)
            detail_url = row[0][0].attrib['href']
            detail_page = self.lxmlize(detail_url)
            photo_url = detail_page.xpath('//img[@class="photoDepute"]/@src')[0]
            division = division.replace('–', '—')  # n-dash, m-dash
            p = Person(primary_org='legislature', name=name, district=division, role='MNA',
                       party=party, image=photo_url)
            p.add_source(COUNCIL_PAGE)
            p.add_source(detail_url)
            if email:
                p.add_contact('email', email)
            contact_url = detail_url.replace('index.html', 'coordonnees.html')
            contact_page = self.lxmlize(contact_url)
            p.add_source(contact_url, note='For telephone number(s)')
            for div in contact_page.xpath('//div[@class="blockAdresseDepute"]'):
                try:
                    phone = self.get_phone(div)
                    heading = div.find('h3').text
                except Exception:
                    pass  # probably just no phone number present
                else:
                    try:
                        note = {
                            'Circonscription': 'constituency',
                            'Parlement': 'legislature',
                            'Ministère': 'legislature',
                        }[heading]
                    except KeyError:
                        raise  # scraper should be updated to handle new value
                    else:
                        p.add_contact('voice', phone, note)
            yield p
