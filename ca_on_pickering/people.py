import re

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.pickering.ca/council-city-administration/mayor-and-council/"


class PickeringPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        cards = page.xpath('//div[contains(@class, "text base-text")][.//a[contains(., "Profile")]]')
        assert len(cards), "No council member cards found"
        for card in cards:
            name = card.xpath(".//strong//text()")[0].strip()
            profile_url = card.xpath('.//a[contains(., "Profile")]/@href')[0]
            email = self.get_email(card)

            if "Mayor" in name:
                name = re.sub(r"^Mayor\s+", "", name)
                role, district = "Mayor", "Pickering"
            else:
                name = re.sub(r"^Councillor\s+", "", name)
                text = re.sub(r"\s+", " ", card.text_content())
                match = re.search(r"(Regional|City) Councillor\s*[-–]?\s*(Ward \d+)", text)
                # The city's "City Councillor" corresponds to the "Councillor" post.
                role = "Regional Councillor" if match.group(1) == "Regional" else "Councillor"
                district = match.group(2)

            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)
            p.add_source(profile_url)
            p.add_contact("email", email)

            profile = self.lxmlize(profile_url)
            image = profile.xpath('//main//img[not(contains(@src, "logo") or contains(@src, "icon"))]/@src')
            if image:
                p.image = image[0]
            # Only some profiles publish a direct line, in a signature
            # paragraph ending in "City of Pickering"; the rest of the page
            # only has the generic switchboard number.
            for signature in profile.xpath('//main//p[contains(., "City of Pickering")]'):
                match = re.search(r"\d{3}[.\-\s]\d{3}[.\-\s]\d{4}", signature.text_content())
                if match:
                    p.add_contact("voice", match.group(0).replace(".", "-"), "legislature")
                    break

            yield p
