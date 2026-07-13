from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.ville.boisbriand.qc.ca/ville/vie-democratique/conseil-municipal"

MEMBERS = [
    ("Christine Beaudette", "Mairesse", "Boisbriand", None),
    ("Maude Whittom", "Conseiller", "District 1", "mwhittom@ville.boisbriand.qc.ca"),
    ("Josée Perrier", "Conseiller", "District 2", "jperrier@ville.boisbriand.qc.ca"),
    ("Chantal Vaillancourt", "Conseiller", "District 3", "cvaillancourt@ville.boisbriand.qc.ca"),
    ("Jonathan Thibault", "Conseiller", "District 4", "jthibault@ville.boisbriand.qc.ca"),
    ("Daniel Kaeser", "Conseiller", "District 5", "dkaeser@ville.boisbriand.qc.ca"),
    ("Cindy Germain", "Conseiller", "District 6", "cgermain@ville.boisbriand.qc.ca"),
    ("Patrick Thifault", "Conseiller", "District 7", "pthifault@ville.boisbriand.qc.ca"),
    ("Lori Doucet", "Conseiller", "District 8", "ldoucet@ville.boisbriand.qc.ca"),
]


class BoisbriandPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE, "utf-8", verify=False)
        for name, role, district, email in MEMBERS:
            image = page.xpath(
                f'//img[contains(@src, "{name.split()[0]}") or contains(@src, "{name.split()[-1]}")]/@src'
            )
            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)
            if email:
                p.add_contact("email", email)
            if image:
                p.image = image[-1]
            yield p
