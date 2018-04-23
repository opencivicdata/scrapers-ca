from utils import CanadianScraper, CanadianPerson as Person

COUNCIL_PAGE = 'https://nslegislature.ca/members/profiles'


class NovaScotiaPersonScraper(CanadianScraper):
    PARTIES = {
        'Liberal': 'Nova Scotia Liberal Party',
        'PC': 'Progressive Conservative Association of Nova Scotia',
        'NDP': 'Nova Scotia New Democratic Party',
    }

    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)
        members = page.xpath('//div[contains(@class, "view-display-id-page_mlas_current_tiles")]//div[contains(@class, "views-row-")]')  # noqa
        assert len(members), 'No members found'
        for member in members:
            district = member.xpath('.//div[contains(@class, "views-field-field-constituency")]/div/text()')[0]
            party = member.xpath('.//span[contains(@class, "party-name")]/text()')[0]

            if party == 'Vacant':
                continue

            detail_url = member.xpath('.//@href')[0]
            detail = self.lxmlize(detail_url)

            name = detail.xpath('//div[contains(@class, "views-field-field-last-name")]/div/h1/text()')[0]
            party = self.PARTIES[party]

            p = Person(primary_org='legislature', name=name, district=district, role='MLA', party=party)
            p.image = detail.xpath('//img[@typeof="foaf:Image"]/@src')[0]

            contact = detail.xpath('//div[contains(@class, "mla-current-profile-contact")]')[0]
            p.add_contact('email', self.get_email(contact))
            p.add_contact('voice', self.get_phone(contact, area_codes=[902]), 'constituency')

            p.add_source(COUNCIL_PAGE)
            p.add_source(detail_url)

            yield p
