import re

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.ville.magog.qc.ca/ville-de-magog/conseil-municipal/"
MEMBERS = [
    ("Nathalie Pelletier", "Maire", "Magog", "n.pelletier@ville.magog.qc.ca"),
    ("Josée Beaudoin", "Conseiller", "District 1", "j.beaudoin@ville.magog.qc.ca"),
    ("Bertrand Bilodeau", "Conseiller", "District 2", "b.bilodeau@ville.magog.qc.ca"),
    ("Nathalie Laporte", "Conseiller", "District 3", "n.laporte@ville.magog.qc.ca"),
    ("Samuel Côté", "Conseiller", "District 4", "s.cote3@ville.magog.qc.ca"),
    ("Marie-Claude Poulin", "Conseiller", "District 5", "m.poulin@ville.magog.qc.ca"),
    ("Guillaume Bouchard", "Conseiller", "District 6", "g.bouchard@ville.magog.qc.ca"),
    ("Jennifer D'Arcy", "Conseiller", "District 7", "j.darcy@ville.magog.qc.ca"),
    ("Simon Mailhot", "Conseiller", "District 8", "s.mailhot@ville.magog.qc.ca"),
]


class MagogPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE, verify=False)
        images = {}
        for img in page.xpath(
            '//img[contains(@alt, "Mairesse") or contains(@alt, "Conseiller") or contains(@alt, "Conseillère") or contains(@src, "District-")]'
        ):
            alt = img.get("alt")
            images[alt.split(" - ")[0].strip()] = img.get("src")
        for name, role, district, email in MEMBERS:
            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)
            p.add_contact("email", email)
            if name in images:
                p.image = images[name]
            yield p
