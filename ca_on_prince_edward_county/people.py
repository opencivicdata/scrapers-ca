from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.thecounty.ca/government/council/"
MEMBERS = [
    ("Steve Ferguson", "Mayor", "Prince Edward County", "sferguson@pecounty.on.ca"),
    ("Kate MacNaughton", "Councillor", "Picton (seat 1)", "kmacnaughton@pecounty.on.ca"),
    ("Phil St-Jean", "Councillor", "Picton (seat 2)", "pst-jean@pecounty.on.ca"),
    ("Brad Nieman", "Councillor", "Bloomfield/Hallowell (seat 1)", "bnieman@pecounty.on.ca"),
    ("Phil Prinzen", "Councillor", "Bloomfield/Hallowell (seat 2)", "pprinzen@pecounty.on.ca"),
    ("Corey Engelsdorfer", "Councillor", "Wellington", "cengelsdorfer@pecounty.on.ca"),
    ("Sam Grosso", "Councillor", "Ameliasburgh (seat 1)", "sgrosso@pecounty.on.ca"),
    ("Janice Maynard", "Councillor", "Ameliasburgh (seat 2)", "jmaynard@pecounty.on.ca"),
    ("Roy Pennell", "Councillor", "Ameliasburgh (seat 3)", "rpennell@pecounty.on.ca"),
    ("Sam Branderhorst", "Councillor", "Athol", "sbranderhorst@pecounty.on.ca"),
    ("Bill Roberts", "Councillor", "Sophiasburgh", "broberts@pecounty.on.ca"),
    ("Chris Braney", "Councillor", "Hillier", "cbraney@pecounty.on.ca"),
    ("David Harrison", "Councillor", "North Marysburgh", "dharrison@pecounty.on.ca"),
    ("John Hirsch", "Councillor", "South Marysburgh", "jhirsch@pecounty.on.ca"),
]


class PrinceEdwardCountyPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE, verify=False)
        image = page.xpath('//img[contains(@src, "Mayor-Ferguson")]/@src')
        for name, role, district, email in MEMBERS:
            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)
            p.add_contact("email", email)
            if role == "Mayor" and image:
                p.image = image[0]
            yield p
