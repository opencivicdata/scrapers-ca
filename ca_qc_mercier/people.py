from utils import CUSTOM_USER_AGENT, CanadianScraper
from utils import CanadianPerson as Person

COUNCIL_PAGE = "https://www.ville.mercier.qc.ca/affaires-municipales/conseil-municipal/membres-du-conseil/"


class MercierPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE, user_agent=CUSTOM_USER_AGENT)

        councillors = page.xpath('//div[@class="wp-block-team-member"]')
        assert len(councillors), "No councillors found"
        for councillor in councillors:
            name = councillor.xpath(".//h4/text()")[0]
            district = councillor.xpath(".//h5/text()")[0].split(" – ")[1]

            email = self.get_email(councillor)
            phone = self.get_phone(councillor)
            image = councillor.xpath(".//img/@src")[0]

            p = Person(primary_org="legislature", name=name, district=district, role="Conseiller", image=image)
            p.add_source(COUNCIL_PAGE)
            p.add_contact("email", email)
            p.add_contact("voice", phone, "legislature")

            yield p

        mayor_node = page.xpath('//div[@class="wp-block-media-text alignwide is-stacked-on-mobile"]')[0]
        name = mayor_node.xpath(".//h1")[0].text_content()

        email = self.get_email(mayor_node)
        phone = self.get_phone(mayor_node)
        image = mayor_node.xpath(".//img/@src")[0]

        p = Person(primary_org="legislature", name=name, district="Mercier", role="Maire", image=image)
        p.add_source(COUNCIL_PAGE)
        p.add_contact("email", email)
        p.add_contact("voice", phone, "legislature")

        yield p
