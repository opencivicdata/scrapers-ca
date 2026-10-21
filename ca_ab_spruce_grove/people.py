import re

from utils import CanadianPerson as Person
from utils import CanadianScraper

LISTING_URL = "https://www.sprucegrove.org/government/city-council/"


class SpruceGrovePersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(LISTING_URL)
        all_links = page.xpath('//a[contains(@href,"/government/city-council/")]/@href')
        member_links = list(dict.fromkeys(h for h in all_links if re.search(r"/(mayor|councillor)-", h)))
        assert member_links, "No member links found"
        seat = 0
        for href in member_links:
            url = href if href.startswith("http") else f"https://www.sprucegrove.org{href}"
            ppage = self.lxmlize(url)
            name_h = ppage.xpath("//h1")
            raw_name = name_h[0].text_content().strip() if name_h else ""
            name = re.sub(r"^(Mayor|Councillor)\s+", "", raw_name).strip()
            if not name:
                continue
            if "/mayor-" in href:
                role, district = "Mayor", "Spruce Grove"
            else:
                seat += 1
                role, district = "Councillor", f"Spruce Grove (seat {seat})"
            email_a = ppage.xpath('.//a[starts-with(@href,"mailto:")]')
            email = email_a[0].get("href").replace("mailto:", "") if email_a else None
            phone_link = ppage.xpath('.//a[starts-with(@href,"tel:")]')
            phone = phone_link[0].text_content().strip() if phone_link else None
            image = ppage.xpath('//img[contains(@src,"/media/")]/@src')
            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(LISTING_URL)
            p.add_source(url)
            if email:
                p.add_contact("email", email)
            if phone:
                p.add_contact("voice", phone, "legislature")
            if image:
                p.image = image[0]
            yield p
