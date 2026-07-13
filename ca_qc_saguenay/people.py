import re

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://ville.saguenay.ca/la-ville-et-vie-democratique/conseils-municipaux-et-darrondissement/membres-des-conseils"
MAYOR_PAGE = "https://ville.saguenay.ca"
CONTACT_PAGE = "https://ville.saguenay.ca/la-ville-et-vie-democratique/cabinet"


class SaguenayPersonScraper(CanadianScraper):
    def scrape(self):
        contact_page = self.lxmlize(CONTACT_PAGE)
        name_paragraph = contact_page.xpath(
            '//h2[contains(., "Coordonn")]/following-sibling::p[contains(., "maire")][1]'
        )[0].text_content()
        name = re.search(r"maire\s+([\wÀ-ž]+\s+[\wÀ-ž]+)", name_paragraph).group(1)
        p = Person(primary_org="legislature", name=name, district="Saguenay", role="Maire")
        p.add_source(MAYOR_PAGE)
        p.add_source(CONTACT_PAGE)
        node = contact_page.xpath('//h2[contains(., "Coordonn")]/following-sibling::p')[1]
        p.add_contact("voice", self.get_phone(node, area_codes=[418]), "legislature")
        yield p

        page = self.lxmlize(COUNCIL_PAGE)
        # Each District N article has all councillors as rows; the first row
        # belongs to District N itself.
        councillors = page.xpath('//article[./h3[starts-with(., "District")]]')
        assert len(councillors), "No councillors found"
        for councillor in councillors:
            district = councillor.xpath("./h3/text()")[0].strip()
            first_row = councillor.xpath(".//table//tr[1]")
            if not first_row:
                continue
            tds = first_row[0].xpath("./td")
            if len(tds) < 2:
                continue
            name_texts = [t.strip() for t in tds[1].itertext() if t.strip()]
            if not name_texts:
                continue
            name = name_texts[0]

            p = Person(primary_org="legislature", name=name, district=district, role="Conseiller")
            p.add_source(COUNCIL_PAGE)
            p.add_contact("voice", self.get_phone(tds[1], area_codes=[418]), "legislature")
            p.add_contact("email", self.get_email(tds[1]))
            yield p
