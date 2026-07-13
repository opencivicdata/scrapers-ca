from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://tofino.ca/your-government/council/mayor-council/"


class TofinoPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE, verify=False)
        members = []
        for img in page.xpath(
            '//img[(contains(@alt, "Mayor") or contains(@alt, "Councillor")) and not(starts-with(@src, "data:"))]'
        ):
            alt = img.get("alt")
            if alt.startswith("Mayor "):
                name = alt.replace("Mayor ", "").strip()
                role, district = "Mayor", "Tofino"
            elif alt.startswith("Councillor "):
                name = alt.replace("Councillor ", "").strip()
                role = "Councillor"
                district = f"Tofino (seat {len([member for member in members if member[1] == 'Councillor']) + 1})"
            else:
                continue
            email = self.get_email(img.getparent(), error=False)
            members.append((name, role, district, email, img.get("src")))

        assert len(members) == 7, "Expected mayor and 6 councillors"
        for name, role, district, email, image in members:
            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)
            if email:
                p.add_contact("email", email)
            p.image = image
            yield p
