from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.courtenay.ca/city-hall/mayor-and-council"
CONTACT_PAGE = "https://www.courtenay.ca/city-hall/mayor-and-council/contact-council"

MEMBERS = [
    ("Bob Wells", "Mayor", "Courtenay"),
    ("David Frisch", "Councillor", "Courtenay (seat 1)"),
    ("Melanie McCollum", "Councillor", "Courtenay (seat 2)"),
    ("Doug Hillian", "Councillor", "Courtenay (seat 3)"),
    ("Will Cole-Hamilton", "Councillor", "Courtenay (seat 4)"),
    ("Wendy Morin", "Councillor", "Courtenay (seat 5)"),
    ("Evan Jolicoeur", "Councillor", "Courtenay (seat 6)"),
]


class CourtenayPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(CONTACT_PAGE, verify=False)
        mayor_image = page.xpath('//img[contains(@alt, "Mayor Bob Wells")]/@src')
        for name, role, district in MEMBERS:
            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)
            p.add_source(CONTACT_PAGE)
            if role == "Mayor" and mayor_image:
                p.image = mayor_image[0]
            yield p
