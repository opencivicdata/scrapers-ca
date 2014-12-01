# coding: utf-8
from __future__ import unicode_literals
from utils import CanadianScraper, CanadianPerson as Person

import hashlib
import json

COUNCIL_PAGE = 'http://www.parl.gc.ca/Parliamentarians/en/members?view=ListAll'
IMAGE_PLACEHOLDER_SHA1 = ['e4060a9eeaf3b4f54e6c16f5fb8bf2c26962e15d']


class CanadaPersonScraper(CanadianScraper):

    """
    The CSV at http://www.parl.gc.ca/Parliamentarians/en/members/export?output=CSV
    accessible from http://www.parl.gc.ca/Parliamentarians/en/members has no
    contact information or photo URLs.
    """

    def scrape(self):
        screen_names = json.loads(self.get('http://scrapers-ruby.herokuapp.com/twitter_users').text)

        page = self.lxmlize(COUNCIL_PAGE)
        rows = page.xpath('//div[@class="main-content"]//tr')[1:]
        for row in rows:
            name_cell = row.xpath('./td[1]')[0]
            last_name = name_cell.xpath('string(.//span[1])')
            first_name = name_cell.xpath('string(.//span[2])')
            name = '%s %s' % (first_name, last_name)
            constituency = row.xpath('string(./td[2])')
            province = row.xpath('string(./td[3])')
            party = row.xpath('string(./td[4])')
            url = name_cell.xpath('.//a/@href')[0]
            if province == 'Québec':
                url = url.replace('/en/', '/fr/')

            mp_page = self.lxmlize(url)
            email = mp_page.xpath('string(//span[@class="caucus"]/'
                                  'a[contains(., "@")])')
            photo = mp_page.xpath('string(//div[@class="profile overview header"]//'
                                  'img/@src)')

            m = Person(primary_org='lower', name=name, district=constituency, role='MP', party=party)
            m.add_source(COUNCIL_PAGE)
            m.add_source(url)
            screen_name = screen_names.get(name)
            if screen_name:
                m.add_link('https://twitter.com/%s' % screen_name)
            # @see http://www.parl.gc.ca/Parliamentarians/en/members/David-Yurdiga%2886260%29
            if email:
                m.add_contact('email', email)
            elif name == 'Adam Vaughan':
                m.add_contact('email', 'Adam.Vaughan@parl.gc.ca')

            if photo:
                # Determine whether the photo is actually a generic silhouette
                photo_response = self.get(photo)
                if (photo_response.status_code == 200 and hashlib.sha1(photo_response.content).hexdigest() not in IMAGE_PLACEHOLDER_SHA1):
                    m.image = photo

            personal_url = mp_page.xpath('//a[contains(@title, "Personal Web Site")]/@href')
            if personal_url:
                m.add_link(personal_url[0])

            if province == 'Québec':
                m.add_contact('address', 'Chambre des communes\nOttawa ON  K1A 0A6', 'legislature')
            else:
                m.add_contact('address', 'House of Commons\nOttawa ON  K1A 0A6', 'legislature')
            voice = mp_page.xpath('string(//div[@class="hilloffice"]//span[contains(text(), "Telephone:")])')
            if voice:
                m.add_contact('voice', voice.replace('Telephone: ', ''), 'legislature')
            fax = mp_page.xpath('string(//div[@class="hilloffice"]//span[contains(text(), "Fax:")])').replace('Fax: ', '')
            if fax:
                m.add_contact('fax', fax, 'legislature')

            for i, li in enumerate(mp_page.xpath('//div[@class="constituencyoffices"]//li')):
                spans = li.xpath('./span[not(@class="spacer")]')
                note = 'constituency'
                if i:
                    note += ' ({})'.format(i + 1)
                m.add_contact('address', '\n'.join([
                    spans[0].text_content(),  # address line 1
                    spans[1].text_content(),  # address line 2
                    spans[2].text_content(),  # city, region
                    spans[3].text_content(),  # postal code
                ]), note)
                voice = li.xpath('string(./span[contains(text(), "Telephone:")])').replace('Telephone: ', '')
                if voice:
                    m.add_contact('voice', voice, note)
                fax = li.xpath('string(./span[contains(text(), "Fax:")])').replace('Fax: ', '')
                if fax:
                    m.add_contact('fax', fax, note)

            yield m
