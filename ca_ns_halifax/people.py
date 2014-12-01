from __future__ import unicode_literals
from utils import CanadianScraper, CanadianPerson as Person

COUNCIL_PAGE = 'http://www.halifax.ca/councillors/index.html'
MAYOR_PAGE = 'http://www.halifax.ca/mayor/'
MAYOR_CONTACT_URL = 'http://www.halifax.ca/mayor/contact.php'


class HalifaxPersonScraper(CanadianScraper):

    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE, 'iso-8859-1')
        nodes = page.xpath('//table[@width="484"]//tr')
        try:
            for district_row, councillor_row, contact_row, _ in chunks(nodes, 4):
                district = district_row.xpath('string(.//strong)')
                name = councillor_row.xpath('string(.)')[len('Councillor '):]
                # TODO: phone numbers on site don't include area code. Add manually?
                # phone = contact_row.xpath('td[2]/text()')[0]
                email = contact_row.xpath('string(td[4]/a)').replace('[at]', '@')

                p = Person(primary_org='legislature', name=name, district=district, role='Councillor')
                p.add_source(COUNCIL_PAGE)
                # p.add_contact('voice', phone, 'legislature')
                p.add_contact('email', email)
                yield p
        except ValueError:
            # on the last run through, there will be less than 4 rows to unpack
            pass

        mayor_page = self.lxmlize(MAYOR_PAGE, 'iso-8859-1')
        name = mayor_page.xpath('string(//h1[contains(., "Bio")])')[:-len(' Bio')]
        contact_page = self.lxmlize(MAYOR_CONTACT_URL, 'iso-8859-1')
        email = contact_page.xpath('string(//a[contains(., "@")][1])')

        p = Person(primary_org='legislature', name=name, district='Halifax', role='Councillor')
        p.add_source(MAYOR_PAGE)
        p.add_source(MAYOR_CONTACT_URL)
        p.add_contact('email', email)
        yield p


def chunks(l, n):
    """ Yield successive n-sized chunks from l.
    """
    for i in range(0, len(l), n):
        yield l[i:i + n]
