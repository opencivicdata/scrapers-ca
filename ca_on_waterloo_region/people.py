import re
from collections import defaultdict

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.regionofwaterloo.ca/en/regional-government/council.aspx"


class WaterlooPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        municipalities = page.xpath("//table[1]//tr[not(.//a)]")
        assert len(municipalities), "No municipalities found"

        seat_numbers = defaultdict(int)
        for municipality in municipalities:
            area = municipality.text_content().strip()
            area = re.sub(r"(?:City|Region|Township) of ", "", area)

            councillors = municipality.xpath("./following-sibling::tr[1]//a[not(@target)]")
            assert len(councillors), f"No councillors found for {area}"

            for councillor in councillors:
                name = councillor.text_content()
                url = councillor.xpath("./@href")[0]
                page = self.lxmlize(url)

                if re.search("Waterloo|Cambridge|Kitchener", area):
                    seat_numbers[area] += 1
                    district = f"{area} (seat {seat_numbers[area]})"
                else:
                    district = area
                if "Regional Council" in area:
                    district = "Waterloo"
                    role = "Chair"
                else:
                    role = "Regional Councillor"

                p = Person(primary_org="legislature", name=name, district=district, role=role)
                image = page.xpath('.//img[@class="Right"]/@src')
                if image:
                    p.image = image[0]

                email = self.get_email(page)
                phone = self.get_phone(page)
                links = page.xpath('//div[@id="printArea"]//p[1]//@href[not(contains(., "mail"))]')
                if links:
                    for link in links:
                        p.add_link(link)
                p.add_contact("email", email)
                p.add_contact("voice", phone, "legislature")

                p.add_source(COUNCIL_PAGE)
                p.add_source(url)

                yield p
