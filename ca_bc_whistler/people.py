from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.whistler.ca/mayor-council/your-council/"
CONTACT_PAGE = "https://www.whistler.ca/contact/"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/125 Safari/537.36"
MEMBERS = [
    ("Jack Crompton", "Mayor", "Whistler", "jcrompton@whistler.ca", "Mayor Crompton"),
    ("Arthur DeJong", "Councillor", "Whistler (seat 1)", "adejong@whistler.ca", "Councillor DeJong"),
    ("Jen Ford", "Councillor", "Whistler (seat 2)", "jford@whistler.ca", "Councillor Ford"),
    ("Ralph Forsyth", "Councillor", "Whistler (seat 3)", "rforsyth@whistler.ca", "Councillor Forsyth"),
    ("Cathy Jewett", "Councillor", "Whistler (seat 4)", "cjewett@whistler.ca", "Councillor Jewett"),
    ("Jessie Morden", "Councillor", "Whistler (seat 5)", "jmorden@whistler.ca", "Councillor Morden"),
    ("Jeff Murl", "Councillor", "Whistler (seat 6)", "jmurl@whistler.ca", "Councillor Murl"),
]


class WhistlerPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE, user_agent=USER_AGENT, verify=False)
        contact_page = self.lxmlize(CONTACT_PAGE, user_agent=USER_AGENT, verify=False)
        contact_text = contact_page.text_content()
        assert all(email in contact_text for _, role, _, email, _ in MEMBERS if role != "Mayor"), (
            "Expected all councillor emails on contact page"
        )

        for name, role, district, email, image_alt in MEMBERS:
            image = page.xpath(f'//img[@alt="{image_alt}" and not(starts-with(@src, "data:"))]/@src')
            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)
            p.add_source(CONTACT_PAGE)
            p.add_contact("email", email)
            if image:
                p.image = image[0]
            yield p
