import re

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.fortsask.ca/city-hall/city-council/members-of-city-council/"


class FortSaskatchewanPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE, verify=False)
        images = [src for src in page.xpath("//img/@src") if "mayor-" in src or "councillor-" in src]
        assert images, "No council images found"
        seat = 0
        for image in images:
            filename = image.split("/")[-1].split("?")[0].replace(".jpg", "")
            role_word, *parts = filename.split("-")
            name = " ".join(part.capitalize() for part in parts)
            if role_word == "mayor":
                role, district = "Mayor", "Fort Saskatchewan"
            else:
                seat += 1
                role, district = "Councillor", f"Fort Saskatchewan (seat {seat})"
            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)
            p.image = image
            yield p
