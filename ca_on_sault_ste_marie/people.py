from urllib.parse import urljoin

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "http://www.city.sault-ste-marie.on.ca/Open_Page.aspx?ID=174&deptid=1"


def word_to_number(word):
    words = ("one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten")
    return words.index(word.lower()) + 1


def district_name_using_number(name):
    district_split = name.split()
    return " ".join([district_split[0], str(word_to_number(district_split[1]))])


class SaultSteMariePersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)
        table_data = page.xpath('//div[@id="litcontentDiv"]//tr')
        council_data = table_data[2:-1]

        mayor_row = table_data[0]

        photo_url_rel = mayor_row.xpath("string(.//img/@src)")  # can be empty
        photo_url = urljoin(COUNCIL_PAGE, photo_url_rel)
        contact_node = mayor_row.xpath("./td")[1]
        name = contact_node.xpath(".//font[1]/text()")[0]
        email = self.get_email(contact_node)

        p = Person(primary_org="legislature", name=name, district="Sault Ste. Marie", role="Mayor")
        p.add_source(COUNCIL_PAGE)
        p.add_contact("email", email)
        p.image = photo_url
        yield p

        # alternate between a row represneting a ward name and councilors
        assert len(council_data), "No councillors found"
        for ward_row, data_row in zip(*[iter(council_data)] * 2):
            district = ward_row.xpath('.//text()[contains(., "Ward")]')[0]
            district_num = district_name_using_number(district)
            for councillor_node in data_row.xpath("./td"):
                name = councillor_node.xpath(".//strong/text()|.//font[1]/text()")[0]
                email = self.get_email(councillor_node)
                photo_url_rel = councillor_node.xpath("string(.//img/@src)")  # can be empty
                photo_url = urljoin(COUNCIL_PAGE, photo_url_rel)
                # address and phone are brittle, inconsistent

                p = Person(primary_org="legislature", name=name, district=district_num, role="Councillor")
                p.add_source(COUNCIL_PAGE)
                if email:
                    p.add_contact("email", email)
                p.image = photo_url

                yield p
