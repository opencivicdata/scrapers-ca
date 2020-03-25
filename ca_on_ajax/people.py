from utils import CanadianScraper, CanadianPerson as Person

COUNCIL_PAGE = 'https://www.ajax.ca/en/inside-townhall/council-members.aspx'


class AjaxPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        councillors = page.xpath('//table[@class="councilTable"]')
        assert len(councillors), 'No councillors found'
        for councillor in councillors:
            image = councillor.xpath('.//@src')[0]
            councillor_name = councillor.xpath('.//tr/td[1]/p[1]/img/@alt')[0]
            name = councillor_name.split('-', 1)[0].strip()
            district = councillor_name.split('Councillor ')[-1].strip()

            if 'Mayor' in councillor_name:
                district = 'Ajax'
                role = 'Mayor'

            else:
                role = councillor_name.split('Ward ')[0].strip()
                role = role.split('-', 1)[-1].strip()

            cell = councillor.xpath('.//p[contains(.,"Cel")]/text()')[0]
            tel = councillor.xpath('.//p[contains(.,"Cel")]/text()')[1]
            phone = cell.replace('\xa0', ' ')

            p = Person(primary_org='legislature', name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)
            p.image = image
            email = self.get_email(councillor)

            if phone:
                p.add_contact('cell', phone, 'legislature')
            if tel:
                p.add_contact('voice', tel, 'legislature')
            if email:
                p.add_contact('email', email)
            yield p
