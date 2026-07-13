from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.cornwall.ca/en/government-council/council-and-committees/"


class CornwallPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        mayor_blocks = page.xpath('//div[contains(@class,"text base-text")][.//h2[normalize-space()="Mayor"]]')
        assert mayor_blocks, "Mayor block not found"
        mayor_block = mayor_blocks[0]
        bio_texts = mayor_block.xpath(".//p/text()")
        assert bio_texts, "Mayor bio text not found"
        bio_text = bio_texts[0].strip()
        if "Mayor " in bio_text:
            name = bio_text.split("Mayor ")[1].split(" was")[0].strip()
        else:
            name = bio_text.split()[0:3]
            name = " ".join(name)
        email = self.get_email(mayor_block, error=False)
        phone = self.get_phone(mayor_block, area_codes=[613, 343], error=False)

        p = Person(primary_org="legislature", name=name, district="Cornwall", role="Mayor")
        p.add_source(COUNCIL_PAGE)
        if email:
            p.add_contact("email", email)
        if phone:
            p.add_contact("voice", phone, "legislature")
        yield p

        seat = 0
        for block in page.xpath('//div[contains(@class,"text base-text")][.//h3]'):
            h3_text = block.xpath(".//h3")[0].text_content().strip()
            name = h3_text.replace("Councillor ", "").strip()
            if not name:
                continue
            seat += 1
            district = f"Councillor (seat {seat})"
            email = self.get_email(block, error=False)
            phone = self.get_phone(block, area_codes=[613, 343], error=False)
            image = block.xpath(".//img/@src")

            p = Person(primary_org="legislature", name=name, district=district, role="Councillor")
            p.add_source(COUNCIL_PAGE)
            if email:
                p.add_contact("email", email)
            if phone:
                p.add_contact("voice", phone, "legislature")
            if image:
                p.image = image[0]
            yield p
