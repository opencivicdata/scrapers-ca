from collections import defaultdict

from utils import CanadianPerson as Person
from utils import CanadianScraper

BASE_URL = "https://www.moncton.ca"
MEMBERS_URL = f"{BASE_URL}/en/government/council/members"


class MonctonPersonScraper(CanadianScraper):
    def scrape(self):
        seat_numbers = defaultdict(int)

        listing = self.lxmlize(MEMBERS_URL)
        cards = [
            c
            for c in listing.xpath(
                '//div[contains(@class,"d-flex") and contains(@class,"position-relative") and .//h3]'
                '[.//a[contains(@href,"/members/")]]'
            )
            if len(c.xpath(".//h3//span/text()")) == 1
        ]
        assert len(cards), "No councillor cards found"

        for card in cards:
            name = card.xpath(".//h3//span/text()")[0].strip()
            link = card.xpath('.//a[contains(@href,"/members/")]/@href')[0]
            img = card.xpath(".//img/@src")

            profile = self.lxmlize(link if link.startswith("http") else BASE_URL + link)

            role_el = profile.xpath('//h2[@class="h5 text-black-50 mb-0 me-3"]')
            role_raw = role_el[0].text_content().strip() if role_el else "Councillor"
            # "Deputy Mayor | Councillor" → "Councillor"; "Councillor-at-Large" → "Councillor at Large"
            role = role_raw.split("|")[-1].strip().replace("-", " ")

            ward_badge = profile.xpath(
                '//div[contains(@class,"badge") and contains(@class,"rounded-pill") and contains(text(),"Ward")]'
            )

            if role == "Mayor":
                district = "Moncton"
            elif role == "Councillor at Large":
                seat_numbers["at_large"] += 1
                district = f"Moncton (seat {seat_numbers['at_large']})"
            else:
                ward = ward_badge[0].text_content().strip() if ward_badge else None
                assert ward, f"No ward found for {name}"
                seat_numbers[ward] += 1
                district = f"{ward} (seat {seat_numbers[ward]})"

            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(MEMBERS_URL)

            if img:
                src = img[0]
                p.image = src if src.startswith("http") else BASE_URL + src

            user = profile.xpath('//span[@class="spamspan"]/span[@class="u"]/text()')
            domain = profile.xpath('//span[@class="spamspan"]/span[@class="d"]/text()')
            if user and domain:
                p.add_contact("email", f"{user[0]}@{domain[0]}")

            phone = profile.xpath('//a[starts-with(@href,"tel:")]/@href')
            if phone:
                p.add_contact("voice", p.clean_telephone_number(phone[0].replace("tel:", "")), "legislature")

            yield p
