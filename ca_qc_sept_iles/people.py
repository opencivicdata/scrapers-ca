from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.septiles.ca/fr/membres-du-conseil_92/"
RESULTS_PAGE = "https://www.septiles.ca/V5/elections-2025"
MEMBERS = [
    ("Benoit Méthot", "Maire", "Sept-Îles", "mairie@septiles.ca"),
    ("Josée Pedneault", "Conseiller", "District 1", "josee.pedneault@septiles.ca"),
    ("Martin Langlois", "Conseiller", "District 2", "martin.langlois@septiles.ca"),
    ("Jeannot Vich", "Conseiller", "District 3", "jeannot.vich@septiles.ca"),
    ("Dave Desjardins", "Conseiller", "District 4", "dave.desjardins@septiles.ca"),
    ("Patrick Lelièvre", "Conseiller", "District 5", "patrick.lelievre@septiles.ca"),
    ("Richard Gagnon", "Conseiller", "District 6", "richard.gagnon@septiles.ca"),
    ("Zéa Blackburn", "Conseiller", "District 7", "zea.blackburn@septiles.ca"),
    ("Manon Langlois", "Conseiller", "District 8", "manon.langlois@septiles.ca"),
    ("Daniel Guérault", "Conseiller", "District 9", "daniel.guerault@septiles.ca"),
]


class SeptIlesPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE, "ISO-8859-1", verify=False)
        text = " ".join(page.text_content().split())
        images = {
            src.split("/")[-1].lower().replace("_", " ").split(" web")[0]: src
            for src in page.xpath('//img[contains(@src, "sys_small")]/@src')
        }

        assert all(email in text for _, _, _, email in MEMBERS), "Expected all Sept-Îles emails on page"
        for name, role, district, email in MEMBERS:
            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)
            p.add_source(RESULTS_PAGE)
            p.add_contact("email", email)
            key = name.lower().replace("é", "e").replace("è", "e").replace("î", "i")
            for image_key, image in images.items():
                if all(part in image_key for part in key.split()):
                    p.image = image
                    break
            yield p
