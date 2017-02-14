from utils import CanadianScraper, CanadianPerson as Person

import re

# Members page load members with javascript
COUNCIL_PAGE = 'https://www.leg.bc.ca/Pages/BCLASS-Category-MLASeatingPlan.aspx'


class BritishColumbiaPersonScraper(CanadianScraper):

    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        members = page.xpath('//table[@cellpadding="4"]//td//a[text()!=""]/@href')
        assert len(members), 'No members found'
        for member in members:
            page = self.lxmlize(member)
            # Hon. is followed by Dr. in one case but the clean_name function
            # removes only one honorific title
            name = page.xpath('//h2[contains(text(), "MLA:")]')[0].text_content().replace('MLA:', '').replace('Dr.', '').replace(', Q.C.', '').replace('Wm.', '').strip()
            district, party = cleanup_list(page.xpath('//h2/following-sibling::div[1]/div[2]/div[1]/div/text()'))
            p = Person(primary_org='legislature', name=name, district=district, role='MLA', party=party)
            p.add_source(COUNCIL_PAGE)
            p.add_source(member)

            p.image = page.xpath('//img[contains(@src, "Members")]/@src')[0]

            email = page.xpath('//span[@class="convertToEmail"]//text()')[0].strip()
            if '#' in email:
                email = email.split('#')[0]
            if email:
                p.add_contact('email', email)

            office = ', '.join(cleanup_list(page.xpath('//h4[contains(text(), "Office:")]/ancestor::div/text()')))
            office = re.sub(r'\s{2,}', ' ', office)
            p.add_contact('address', office, 'legislature')

            constituency = ', '.join(cleanup_list(page.xpath('//h4[contains(text(), "Constituency:")]/ancestor::div[1]//text()')))
            constituency = re.sub(r'\s{2,}', ' ', constituency).split(', Phone')[0]
            p.add_contact('address', constituency, 'constituency')

            phones = cleanup_list(page.xpath('//span[contains(text(), "Phone:")]/following-sibling::text()'))
            faxes = cleanup_list(page.xpath('//span[contains(text(), "Fax:")]/following-sibling::span[1]/text()'))

            office_phone = phones[0]
            p.add_contact('voice', office_phone, 'legislature')
            if len(phones) > 1:
                constituency_phone = phones[1]
                p.add_contact('voice', constituency_phone, 'constituency')
            office_fax = faxes[0]
            p.add_contact('fax', office_fax, 'legislature')
            if len(faxes) > 1:
                constituency_fax = faxes[1]
                p.add_contact('fax', constituency_fax, 'constituency')

            yield p


def cleanup_list(dirty_list):
    return list(filter(None, (x.strip() for x in dirty_list)))
