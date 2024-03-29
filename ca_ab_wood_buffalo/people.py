from collections import defaultdict

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "http://www.woodbuffalo.ab.ca/Municipal-Government/Mayor-and-Council/Councillor-Profiles.htm"


class WoodBuffaloPersonScraper(CanadianScraper):
    def scrape(self):
        seat_numbers = defaultdict(int)

        page = self.lxmlize(COUNCIL_PAGE)

        mayor_url = page.xpath('//li[@id="pageid1075"]/div/a/@href')[0]
        yield self.scrape_mayor(mayor_url)

        wards = page.xpath('//div[@id="content"]//h3')
        assert len(wards), "No wards found"
        for ward in wards:
            area = ward.text_content()
            councillors = ward.xpath("./following-sibling::ul[1]//a")

            assert len(councillors), "No councillors found for ward {}".format(area)
            for councillor in councillors:
                name = " ".join(reversed(councillor.text.split(", ")))
                url = councillor.attrib["href"]

                if area in ("Ward 1", "Ward 2"):
                    seat_numbers[area] += 1
                    district = "{} (seat {})".format(area, seat_numbers[area])
                else:
                    district = area

                p = Person(primary_org="legislature", name=name, district=district, role="Councillor")
                p.add_source(COUNCIL_PAGE)
                p.add_source(url)

                page = self.lxmlize(url)
                p.image = page.xpath('//div[@id="content"]//img[contains(@alt, "Councillor")]/@src')[0]

                email = self.get_email(page.xpath('//div[@id="content"]')[0])
                p.add_contact("email", email)

                yield p

    def scrape_mayor(self, url):
        page = self.lxmlize(url)
        name = page.xpath('//h1[@id="pagetitle"]/text()')[0].replace("Mayor", "").strip()
        image = page.xpath('//div[@id="content"]//@src')[0]

        p = Person(primary_org="legislature", name=name, district="Wood Buffalo", role="Mayor")
        p.add_source(url)

        p.image = image
        p.add_contact("voice", self.get_phone(page.xpath('//div[@id="icon5"]')[0]), "legislature")
        p.add_contact("email", "mayor@rmwb.ca")

        return p
