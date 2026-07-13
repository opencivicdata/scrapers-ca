from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.dieppe.ca/en/hotel-de-ville/maire-et-conseil-municipal/"
SWEARING_IN_PAGE = "https://www.dieppe.ca/en/news/posts/council-swearing-in-ceremony/"
MEMBERS = [
    ("Hélène Boudreau", "Mayor", "Dieppe"),
    ("Mélyssa Boudreau-Janin", "Councillor at Large", "Dieppe (seat 1)"),
    ("Jacob Levesque", "Councillor at Large", "Dieppe (seat 2)"),
    ("Mark Black", "Councillor at Large", "Dieppe (seat 3)"),
    ("Jean-Marc Brideau", "Councillor", "Ward 1"),
    ("Gille Savoie", "Councillor", "Ward 2"),
    ("Marc Lanteigne", "Councillor", "Ward 3"),
    ("Philippe Caouette", "Councillor", "Ward 4"),
    ("Roger LeBlanc", "Councillor", "Ward 5"),
]


class DieppePersonScraper(CanadianScraper):
    def scrape(self):
        self.lxmlize(COUNCIL_PAGE, verify=False)
        for name, role, district in MEMBERS:
            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)
            p.add_source(SWEARING_IN_PAGE)
            yield p
