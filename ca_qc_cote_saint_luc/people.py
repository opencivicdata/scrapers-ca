from utils import CUSTOM_USER_AGENT, CanadianScraper
from utils import CanadianPerson as Person

COUNCIL_PAGE = "https://cotesaintluc.org/fr/affaires-municipales/membres-du-conseil/"


class CoteSaintLucPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE, user_agent=CUSTOM_USER_AGENT)
        councillors = page.xpath('//div/div[contains(@class, "gb-container gb-container-") and .//img]')
        assert len(councillors), "No councillors found"

        for councillor in councillors:
            name, role, district = councillor.xpath("./p[2]//text()")[:3]

            if role == "Maire":
                district = "Côte-Saint-Luc"
            else:
                role = role.replace(", ", "")
                if role == "Conseillère":
                    role = "Conseiller"

            image = councillor.xpath(".//img/@src")[0]
            twitter = self.get_link(councillor, "twitter", error=False)
            facebook = self.get_link(councillor, "facebook", error=False)
            web = councillor.xpath(
                './/p[contains(.,"Web") or contains(., "web")]//@href[not(contains(., "twitter") or contains(., "facebook"))]'
            )
            blog = councillor.xpath(
                './/p[contains(.,"Blog")]//@href[not(contains(., "twitter") or contains(., "facebook"))]'
            )

            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)

            p.add_contact("email", self.get_email(councillor))
            p.add_contact("voice", self.get_phone(councillor, area_codes=[514]), "legislature")
            p.image = image
            if twitter:
                p.add_link(twitter)
            if facebook:
                p.add_link(facebook)
            if web:
                p.add_link(web[0])
            if blog:
                p.add_link(blog[0])

            yield p
