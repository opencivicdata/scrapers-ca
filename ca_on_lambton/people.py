from utils import CanadianScraper, CanadianPerson as Person

COUNCIL_PAGE = 'http://www.lambtononline.ca/home/government/accessingcountycouncil/countycouncillors/Pages/default.aspx'


class LambtonPersonScraper(CanadianScraper):

    def scrape(self):
        councillor_seat_number = 1

        page = self.lxmlize(COUNCIL_PAGE)

        # Tableception here, first tr is left column, second the right column
        councillors_left = page.xpath('//div[@id="content"]/table/tr/td[1]/table/tr')
        councillors_right = page.xpath('//div[@id="content"]/table/tr/td[2]/table/tr')
        councillors = councillors_left + councillors_right
        assert len(councillors), 'No councillors found'
        for councillor in councillors:
            node = councillor.xpath('.//tr[1]')
            text = node[0].text_content()
            if 'Deputy Warden' in text:
                role = 'Deputy Warden'
                name = text.replace('Deputy Warden', '')
                district = 'Lambton'
            elif 'Warden' in text:
                role = 'Warden'
                name = text.replace('Warden', '')
                district = 'Lambton'
            else:
                role = 'Councillor'
                name = text
                district = 'Lambton (seat {})'.format(councillor_seat_number)
                councillor_seat_number += 1

            p = Person(primary_org='legislature', name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)

            p.image = councillor.xpath('.//img/@src')[0]
            p.add_contact('email', self.get_email(councillor))

            yield p
