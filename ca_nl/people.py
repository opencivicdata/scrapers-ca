# coding: utf-8
from utils import CanadianScraper, CanadianPerson as Person

COUNCIL_PAGE = 'http://www.assembly.nl.ca/members/cms/membersalpha.htm'

PARTIES = {
    'Progressive Conservative': 'Progressive Conservative Party of Newfoundland and Labrador',
    'New Democrat': 'New Democratic Party of Newfoundland and Labrador',
    'Liberal': 'Liberal Party of Newfoundland and Labrador',
    'Independent/Non-Affiliated': 'Independent/Non-Affiliated',
}

PHONE_TD_HEADINGS = {
    'legislature': "Confederation Building Office",
    'constituency': "Constituency Office",
}


class NewfoundlandAndLabradorPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)
        members = page.xpath('//div[@id="content"]/table//tr')[1:]
        assert len(members), 'No members found'
        for row in members:
            member_url = row[0].xpath('./a/@href')[0]
            name = row[0].text_content().strip()
            party = row[2].text_content().strip()
            assert party in PARTIES, "unexpected party %s" % party
            party = PARTIES[party]
            district = row[1].text_content().strip()
            district = district.replace(' - ', '—')  # m-dash

            member_page = self.lxmlize(member_url)
            email = self.get_email(member_page.xpath('//div[@id="content"]')[0])
            photo_url = member_page.xpath('//div[@id="content"]//img/@src')[0]

            p = Person(primary_org='legislature', name=name,
                       district=district, role='MHA', party=party)

            p.add_contact('email', email)
            p.add_source(COUNCIL_PAGE)
            p.add_source(member_url)
            p.image = photo_url

            for key, heading in PHONE_TD_HEADINGS.items():
                td = member_page.xpath('//*[.="{0}"]/ancestor::td'.format(heading))
                if td:
                    phone = self.get_phone(td[0], error=False)
                    if phone:
                        p.add_contact('voice', phone, key)
            yield p
