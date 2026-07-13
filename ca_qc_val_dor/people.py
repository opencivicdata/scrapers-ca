from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://ville.valdor.qc.ca/conseil-municipal"


class ValDorPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)
        images = [
            image
            for image in page.xpath("//img[@alt]")
            if image.get("alt") and image.get("alt") not in ("spinner", "Ville de Val-d'Or")
        ]
        members = [image for image in images if "/uploads/team/image/" in image.get("src", "")]
        assert len(members) == 9, "Expected 9 council members"

        for index, image in enumerate(members):
            name = image.get("alt").strip()
            if index == 0:
                role = "Maire"
                district = "Val-d'Or"
            else:
                role = "Conseiller"
                district = f"District {index}"

            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)
            p.image = image.get("src")
            yield p
