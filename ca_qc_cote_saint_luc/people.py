from utils import CUSTOM_USER_AGENT
from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://cotesaintluc.org/fr/affaires-municipales/membres-du-conseil/"


class CoteSaintLucPersonScraper(CanadianScraper):
    def scrape(self):
        def decode_email(e):
            de = ""
            k = int(e[:2], 16)

            for i in range(2, len(e) - 1, 2):
                de += chr(int(e[i : i + 2], 16) ^ k)

            return de

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
            encrypted_email = councillor.xpath('.//@href[contains(., "email")]')[0].split("#")[1]
            email = decode_email(encrypted_email)

            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)

            p.add_contact("email", email)
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
