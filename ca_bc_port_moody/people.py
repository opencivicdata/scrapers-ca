from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.portmoody.ca/city-government/council/"


class PortMoodyPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE, verify=False)
        members = []
        for img in page.xpath('//img[contains(@alt, "Mayor") or contains(@alt, "Councillor")]'):
            alt = img.get("alt")
            if "Mayor" in alt:
                role, district = "Mayor", "Port Moody"
                name = alt.replace("Mayor", "").strip()
            else:
                role = "Councillor"
                district = f"Port Moody (seat {len([m for m in members if m[1] == 'Councillor']) + 1})"
                name = alt.replace("Councillor", "").strip()
                if name == "Agtarap":
                    name = "Samantha Agtarap"
                if name == "Amy":
                    name = "Amy Lubik"
            email = self.get_email(img.getparent(), error=False)
            image = img.get("src")
            members.append((name, role, district, email, image))

        assert members, "No council members found"
        for name, role, district, email, image in members:
            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)
            if email:
                p.add_contact("email", email)
            if image:
                p.image = image
            yield p
