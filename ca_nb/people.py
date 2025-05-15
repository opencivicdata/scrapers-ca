from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.legnb.ca/en/members/current"  # update each election


class NewBrunswickPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE, encoding="utf-8")
        members = page.xpath('//div[contains(@class, "member-card")]//a//@href')
        assert len(members), "No members found"

        for url in members:
            district_corrections = {
                # Accent
                "Shippagan-Lam\u00eaque-Miscou": "Shippagan-Lamèque-Miscou",
                # Capitalization
                "Madawaska Les lacs-Edmundston": "Madawaska Les Lacs-Edmundston",
                "Shippagan-les-\u00celes": "Shippagan-Les-Îles",
                # Hyphenation
                "Bathurst East-Nepisiguit-Saint Isidore": "Bathurst East-Nepisiguit-Saint-Isidore",
                "Fundy-The-Isles-Saint John West": "Fundy-The Isles-Saint John West",
                "Saint John-East": "Saint John East",
            }

            node = self.lxmlize(url, encoding="utf-8")

            email = ""
            phone = ""
            fax = ""

            address = node.xpath('//td[contains(text(),"Address")]/parent::tr//td[2]')
            if address:
                address = [line.strip() for line in address[0].text_content().strip().splitlines()]

            hrefs = node.xpath('//table[contains(@class, "properties-table")]//a//@href')
            for href in hrefs:
                if href.startswith("mailto:"):
                    email = href.replace("mailto:", "")
                if href.startswith("tel:"):
                    phone = href.replace("tel:", "")
                if href.startswith("fax:"):
                    fax = href.replace("fax:", "")

            party, district = [
                span.text_content().strip()
                for span in node.xpath('//div[contains(@class, "member-details-meta")]//span')
            ]

            district = district.replace("\x97", "-").replace(" - ", "-")
            district = district_corrections.get(district, district)

            name = node.xpath("//h1")[0].text_content().replace(", Q.C.", "").replace(", K.C.", "")
            photo_url = node.xpath('//div[contains(@class, "member-details-portrait")]//img//@src')[0]
            roles = node.xpath('//ul[@class="member-details-positions"]/li/text()')

            p = Person(
                primary_org="legislature", name=name, district=district, role="MLA", party=party, image=photo_url
            )
            if email:
                p.add_contact("email", email)
            if phone:
                p.add_contact("voice", phone, "constituency")
            if fax:
                p.add_contact("fax", fax, "legislature")
            if address:
                p.add_contact("address", "\n".join(address), "constituency")
            if roles:
                p.extras["roles"] = [role.strip() for role in roles]

            p.add_source(url)
            yield p
