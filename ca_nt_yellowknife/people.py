import codecs
import re

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.yellowknife.ca/city-council-and-mayor"


class YellowknifePersonScraper(CanadianScraper):
    def decode_email(self, node):
        encoded = node.xpath(".//a[@data-mail-to]/@data-mail-to")
        if not encoded:
            return None
        return codecs.decode(encoded[0], "rot_13").replace("/at/", "@").replace("/dot/", ".")

    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)
        rows = page.xpath('//h2[contains(., "Contact Council")]/following::table[1]//tbody/tr')
        assert len(rows), "No council member rows found"

        images = {}
        for image in page.xpath('//img[contains(@alt, "Portrait Photo of ")]'):
            alt = image.get("alt").replace("Portrait Photo of ", "").strip()
            images[alt] = image.get("src")

        seat = 0
        for row in rows:
            member_text = row.xpath("string(./td[1])").strip()
            if not member_text or member_text == "All Members of Council":
                continue

            if member_text.startswith("Mayor "):
                role = "Mayor"
                name = member_text[len("Mayor ") :]
                district = "Yellowknife"
            else:
                seat += 1
                role = "Councillor"
                district = f"Yellowknife (seat {seat})"
                name = re.sub(r"^(?:Councillor|Deputy Mayor)\s+", "", member_text)

            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)

            email = self.decode_email(row)
            if email:
                p.add_contact("email", email)
            if member_text in images:
                p.image = images[member_text]

            yield p
