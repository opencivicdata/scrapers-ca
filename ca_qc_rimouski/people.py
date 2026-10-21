import re

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://rimouski.ca/ville/democratie/conseil-municipal"


class RimouskiPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)
        cards = page.xpath("//li[@class='withThumb']")
        assert len(cards), "No council member cards found"

        for card in cards:
            h4 = card.xpath(".//h4/text()")
            h6 = card.xpath(".//h6/text()")
            if not h4 or not h6:
                continue

            name = h4[0].strip()
            h6_text = h6[0].strip()

            if "Mairie" in h6_text:
                role = "Mayor"
                district = "Rimouski"
            else:
                m = re.match(r"District (\d+)", h6_text)
                role = "Councillor"
                district = f"District {m.group(1)}" if m else h6_text

            email_links = card.xpath(".//a[starts-with(@href,'mailto:') and not(contains(@href,'?Subject='))]/@href")
            email = email_links[0].replace("mailto:", "") if email_links else None
            phone = self.get_phone(card, area_codes=[418], error=False)
            image = card.xpath(".//picture/img/@src")

            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)
            if email:
                p.add_contact("email", email)
            if phone:
                p.add_contact("voice", phone, "legislature")
            if image:
                p.image = image[0]
            yield p
