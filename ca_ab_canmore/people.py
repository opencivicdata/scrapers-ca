from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.canmore.ca/your-government/council/your-council"
MEMBERS = [
    ("Sean Krausert", "Mayor", "Canmore", "sean.krausert@canmore.ca", "mayorseankrausert"),
    ("Tanya Foubert", "Councillor", "Canmore (seat 1)", "tanya.foubert@canmore.ca", "councillortanyafoubert"),
    ("Wade Graham", "Councillor", "Canmore (seat 2)", "wade.graham@canmore.ca", "councillorwadegraham"),
    ("Jeff Hilstad", "Councillor", "Canmore (seat 3)", "jeff.hilstad@canmore.ca", "councillorjeffhilstad"),
    ("Jeff Mah", "Councillor", "Canmore (seat 4)", "jeff.mah@canmore.ca", "mediumcouncillormah"),
    ("Jen Marran", "Councillor", "Canmore (seat 5)", "jen.marran@canmore.ca", "councillorjenmarran"),
    ("Rob Murray", "Councillor", "Canmore (seat 6)", "rob.murray@canmore.ca", "councillorrobmurray"),
]


class CanmorePersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE, verify=False)
        for name, role, district, email, image_key in MEMBERS:
            image = page.xpath(f'//img[contains(@src, "{image_key}")]/@src')
            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)
            p.add_contact("email", email)
            if image:
                p.image = image[0]
            yield p
