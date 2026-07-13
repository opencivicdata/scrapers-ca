from collections import defaultdict
from urllib.parse import urljoin

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.peterborough.ca/council-city-hall/mayor-and-council/"


class PeterboroughPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        mayor_section = page.xpath(
            '//section[contains(@class, "usn_cmp_splitcomponent")][.//a[contains(@href, "mayor@peterborough.ca")]]'
        )[0]
        yield self.make_person(mayor_section, "Peterborough")

        seat_numbers = defaultdict(int)
        ward_sections = page.xpath(
            '//section[contains(concat(" ", normalize-space(@class), " "), " usn_cmp_pods ")]'
            '[.//h2[starts-with(normalize-space(), "Ward ")]]'
        )
        assert len(ward_sections) == 5, "Expected 5 ward sections"

        for section in ward_sections:
            ward = section.xpath("normalize-space(.//h2)")
            members = section.xpath(
                './/div[contains(concat(" ", normalize-space(@class), " "), " item_text-below ")]'
                '[.//a[contains(@href, "mailto:")]]'
            )
            assert len(members) == 2, f"Expected 2 councillors for {ward}"

            for member in members:
                seat_numbers[ward] += 1
                yield self.make_person(member, f"{ward} (seat {seat_numbers[ward]})")

    def make_person(self, member, district):
        title = member.xpath('normalize-space(.//p[contains(@class, "heading")][1])')
        role, name = title.split(" ", 1)

        p = Person(primary_org="legislature", name=name, district=district, role=role)
        p.add_source(COUNCIL_PAGE)

        image = member.xpath(".//img/@src")
        if image:
            p.image = urljoin(COUNCIL_PAGE, image[0])

        email = self.get_email(member, error=False)
        if email:
            p.add_contact("email", email)

        phone = self.get_phone(member, area_codes=[705, 249, 683], error=False)
        if phone:
            p.add_contact("voice", phone, "legislature")

        return p
