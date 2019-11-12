# coding: utf-8
from utils import CanadianScraper, CanadianPerson as Person
#from pprint import pprint

import hashlib

COUNCIL_PAGE = 'https://www.ourcommons.ca/Members/en/search?view=ListAll'
IMAGE_PLACEHOLDER_SHA1 = ['e4060a9eeaf3b4f54e6c16f5fb8bf2c26962e15d']


class CanadaPersonScraper(CanadianScraper):

    """
    The CSV at http://www.parl.gc.ca/Parliamentarians/en/members/export?output=CSV
    accessible from http://www.parl.gc.ca/Parliamentarians/en/members has no
    contact information or photo URLs.
    """

    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)
        rows = page.xpath('//div[@class="ce-mip-mp-tile-container"]')[1:]
        assert len(rows), 'No members found'
        for row in rows:
            name = row.xpath('.//div[@class="ce-mip-mp-name"][1]')[0].text_content()
            #pprint(name)
            constituency = row.xpath('.//div[@class="ce-mip-mp-constituency"][1]')[0].text_content()
            constituency = constituency.replace('–', '—')  # n-dash, m-dash
            if constituency == 'Mont-Royal':
                constituency = 'Mount Royal'

            province = row.xpath('.//div[@class="ce-mip-mp-province"][1]')[0].text_content()

            party = row.xpath('.//div[@class="ce-mip-mp-party"][1]')[0].text_content()

            url = row.xpath('.//a[@class="ce-mip-mp-tile"]/@href')[0]
            #pprint(url)
            if province == 'Québec':
                url = url.replace('/en/', '/fr/')

            mp_page = self.lxmlize(url)
            email = self.get_email(mp_page, '//*[@id="contact"]/div/p/a', error=False)
            #pprint(email)

            photo = mp_page.xpath('.//div[@class="ce-mip-mp-profile-container"]//img/@src')[0]
            #pprint(photo)

            m = Person(primary_org='lower', name=name, district=constituency, role='MP', party=party)
            m.add_source(COUNCIL_PAGE)
            m.add_source(url)
            # @see https://www.ourcommons.ca/Members/en/ziad-aboultaif(89156)
            if email:
                m.add_contact('email', email)
            # Adam Vaughan's email has been fixed on the new site.
            # elif name == 'Adam Vaughan':
            #     m.add_contact('email', 'Adam.Vaughan@parl.gc.ca')

            if photo:
                # Determine whether the photo is actually a generic silhouette
                photo_response = self.get(photo)
                if (photo_response.status_code == 200 and hashlib.sha1(photo_response.content).hexdigest() not in IMAGE_PLACEHOLDER_SHA1):
                    m.image = photo

            # I don't think the new parliment website has personal website anymore
            personal_url = mp_page.xpath('.//a[contains(@title, "Personal Web Site")]/@href')
            if personal_url:
                m.add_link(personal_url[0])
                #pprint(personal_url[0])

            preferred_languages = mp_page.xpath('.//dt[contains(., "Preferred Language")]/following-sibling::dd/text()')
            if preferred_languages:
                m.extras['preferred_languages'] = [language.replace('/', '').strip() for language in preferred_languages]

            if province == 'Québec':
                m.add_contact('address', 'Chambre des communes\nOttawa ON  K1A 0A6', 'legislature')
            else:
                m.add_contact('address', 'House of Commons\nOttawa ON  K1A 0A6', 'legislature')

            # Hill Office contacts
            # Now phone and fax are in the same element
            # <p>
            #   Telephone: xxx-xxx-xxxx<br/>
            #   Fax: xxx-xxx-xxx
            # </p>
            phone_and_fax_el = mp_page.xpath('.//h4[contains(., "Hill Office")]/../p[contains(., "Telephone")]|.//h4[contains(., "Hill Office")]/../p[contains(., "Téléphone :")]')
            if len(phone_and_fax_el):
                phone_and_fax = phone_and_fax_el[0].text_content().strip().splitlines()
                voice = phone_and_fax[0].replace('Telephone:', '').replace('Téléphone :', '').strip()
                fax = phone_and_fax[1].replace('Fax:', '').replace('Télécopieur :', '').strip()
                #pprint(voice)
                #pprint(fax)
                if voice:
                    m.add_contact('voice', voice, 'legislature')

                if fax:
                    m.add_contact('fax', fax, 'legislature')

            # Constituency Office contacts
            # Some people has more than one, e.g. https://www.ourcommons.ca/Members/en/ben-lobb(35600)#contact
            for i,constituency_office_el in enumerate(mp_page.xpath('.//div[@class="ce-mip-contact-constituency-office-container"]/div')):
                note = 'constituency'
                if i:
                    note += ' ({})'.format(i + 1)

                #pprint(note)
                address = constituency_office_el.xpath('./p[1]')[0]
                address = address.text_content().strip().splitlines()
                address = list(map(str.strip, address))
                #pprint(address)
                m.add_contact('address', '\n'.join(address), note)

                phone_and_fax_el = constituency_office_el.xpath('./p[contains(., "Telephone")]|./p[contains(., "Téléphone")]');
                if len(phone_and_fax_el):
                    phone_and_fax = phone_and_fax_el[0].text_content().strip().splitlines()
                    # Note that https://www.ourcommons.ca/Members/en/michael-barrett(102275)#contact
                    # has a empty value - "Telephone:". So the search / replace cannot include space.
                    voice = phone_and_fax[0].replace('Telephone:', '').replace('Téléphone :', '').strip()
                    if len(phone_and_fax) > 1:
                        fax = phone_and_fax[1].replace('Fax:', '').replace('Télécopieur :', '').strip()

                    if voice:
                        m.add_contact('voice', voice, note)

                    if fax:
                        m.add_contact('fax', fax, note)


            yield m
