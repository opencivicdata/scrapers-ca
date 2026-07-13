import re

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.villethetford.ca/vie-municipale/elus-municipaux/"
MEMBERS = [
    ("Marc-Alexandre Brousseau", "Maire", "Thetford Mines", "ma.brousseau@villethetford.ca"),
    ("Josée Perreault", "Conseiller", "District 1", "j.perreault@villethetford.ca"),
    ("Alexandre Couture", "Conseiller", "District 2", "a.couture@villethetford.ca"),
    ("Adam Patry", "Conseiller", "District 3", "a.patry@villethetford.ca"),
    ("Yvan Corriveau", "Conseiller", "District 4", "y.corriveau@villethetford.ca"),
    ("Émilie Rémillard", "Conseiller", "District 5", "e.remillard@villethetford.ca"),
    ("Frédéric Paré", "Conseiller", "District 6", "f.pare@villethetford.ca"),
    ("Daniel Maheux", "Conseiller", "District 7", "d.maheux@villethetford.ca"),
    ("Jonathan Fillion", "Conseiller", "District 8", "j.fillion@villethetford.ca"),
]


class ThetfordMinesPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE, verify=False)
        for name, role, district, email in MEMBERS:
            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)
            p.add_contact("email", email)
            yield p
