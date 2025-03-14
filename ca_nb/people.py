from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.legnb.ca/en/members/current"  # update each election


class NewBrunswickPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE, encoding="utf-8")
        members = page.xpath('//div[contains(@class, "member-card")]//a//@href')
        assert len(members), "No members found"
        for url in members:
            node = self.lxmlize(url, encoding="utf-8")
            phone = ""
            email = ""
            address = node.xpath('//td[contains(text(),"Address")]/parent::tr//td[2]')[0]
            address = address.text_content().strip().splitlines()
            address = list(map(str.strip, address))
            hrefs = node.xpath('//table[contains(@class, "properties-table")]//a//@href')
            for href in hrefs:
                if href.startswith("mailto:"):
                    email = href.replace("mailto:", "")
                if href.startswith("tel:"):
                    phone = href.replace("tel:", "")

            party, riding = [
                span.text_content().strip()
                for span in node.xpath('//div[contains(@class, "member-details-meta")]//span')
            ]
            district = riding.replace("\x97", "-").replace(" - ", "-")
            if district == "Madawaska Les lacs-Edmundston":
                district = "Madawaska Les Lacs-Edmundston"
            if district == "Fundy-The-Isles-Saint John West":
                district = "Fundy-The Isles-Saint John West"
            if district == "Bathurst East-Nepisiguit-Saint Isidore":
                district = "Bathurst East-Nepisiguit-Saint-Isidore"
            if district == "Shippagan-Lam\u00eaque-Miscou":
                district = "Shippagan-Lamèque-Miscou"
            if district == "Saint John-East":
                district = "Saint John East"
            name = node.xpath("//h1")[0].text_content()
            name = name.replace(", Q.C.", "").replace(", K.C.", "")
            photo_url = node.xpath('//div[contains(@class, "member-details-portrait")]//img//@src')[0]
            roles = node.xpath('//ul[@class="member-details-positions"]/li/text()')

            p = Person(
                primary_org="legislature", name=name, district=district, role="MLA", party=party, image=photo_url
            )
            if phone:
                p.add_contact("voice", phone, "constituency")
            if email:
                p.add_contact("email", email)
            if address:
                p.add_contact("address", "\n".join(address), "constituency")

            if roles:
                p.extras["roles"] = [role.strip() for role in roles]

            p.add_source(url)
            yield p
