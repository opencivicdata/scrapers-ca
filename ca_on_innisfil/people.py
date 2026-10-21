from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_URL = "https://www.innisfil.ca/government-administration/council-committees/members-council"


class InnisfilPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_URL)
        cards = page.xpath('//div[contains(@class, "views-row")][.//h3/a[contains(@href,"/members-council/")]]')
        assert len(cards), "No council member cards found"
        for card in cards:
            name = card.xpath('normalize-space(.//h3/a[contains(@href,"/members-council/")])')
            if not name:
                continue

            pos_text = card.xpath(
                'normalize-space(.//div[contains(@class, "views-field-field-position")]//span[contains(@class, "field-content")])'
            )
            ward_text = card.xpath(
                'normalize-space(.//div[contains(@class, "views-field-field-ward")]//span[contains(@class, "field-content")])'
            )
            if "Mayor" in pos_text and "Deputy" not in pos_text:
                role, district = "Mayor", "Innisfil"
            elif "Deputy Mayor" in pos_text:
                role, district = "Councillor", "Deputy Mayor"
            else:
                role = "Councillor"
                district = ward_text
            email = self.get_email(card, error=False)
            phone_link = card.xpath('.//a[starts-with(@href,"tel:")]')
            phone = phone_link[0].text_content().strip() if phone_link else None
            image = card.xpath(".//img/@src")
            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_URL)
            if email:
                p.add_contact("email", email)
            if phone:
                p.add_contact("voice", phone, "legislature")
            if image:
                p.image = image[0]
            yield p
