from collections import defaultdict

from utils import CanadianPerson as Person
from utils import CanadianScraper

BASE_URL = "https://www.rmwb.ca"
MAYOR_PAGE = f"{BASE_URL}/local-government/mayor-council-and-administration/mayor/"
COUNCILLORS_PAGE = f"{BASE_URL}/local-government/mayor-council-and-administration/council/councillors/"


class WoodBuffaloPersonScraper(CanadianScraper):
    def scrape_mayor(self):
        page = self.lxmlize(MAYOR_PAGE)

        bio = page.xpath('//h2[contains(text(),"Biography")]/following-sibling::p[normalize-space()][1]')
        name = " ".join(bio[0].text_content().strip().split()[:2])

        image = page.xpath("//main//img/@src")

        p = Person(primary_org="legislature", name=name, district="Wood Buffalo", role="Mayor")
        p.add_source(MAYOR_PAGE)
        if image:
            src = image[0]
            p.image = src if src.startswith("http") else BASE_URL + src

        return p

    def scrape(self):
        yield self.scrape_mayor()

        page = self.lxmlize(COUNCILLORS_PAGE)
        tab_blocks = page.xpath('//div[contains(@class,"repeatable accordion")]')
        assert len(tab_blocks), "No councillor accordion blocks found"

        seat_numbers = defaultdict(int)

        for tab_block in tab_blocks:
            h2s = tab_block.xpath('preceding::h2[contains(text(),"Ward")][1]')
            assert h2s, "Could not find ward heading for accordion block"
            ward = h2s[0].text_content().split("–")[-1].strip()  # "Ward 1", "Ward 2", etc.

            names = tab_block.xpath('.//p[@class="tab "]/a/text()')
            contents = tab_block.xpath('.//div[contains(@class,"repeatable-content")]')
            assert len(names) == len(contents), f"Name/content mismatch for {ward}"

            for name, content in zip(names, contents):
                name = name.strip()

                if ward in ("Ward 1", "Ward 2"):
                    seat_numbers[ward] += 1
                    district = f"{ward} (seat {seat_numbers[ward]})"
                else:
                    district = ward

                p = Person(primary_org="legislature", name=name, district=district, role="Councillor")
                p.add_source(COUNCILLORS_PAGE)

                img = content.xpath(".//img/@src")
                if img:
                    src = img[0]
                    p.image = src if src.startswith("http") else BASE_URL + src

                email = content.xpath('.//a[contains(@href,"mailto:")]/@href')
                if email:
                    p.add_contact("email", email[0].replace("mailto:", ""))

                yield p
