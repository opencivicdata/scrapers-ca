from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.wilmot.ca/en/township-office/council.aspx"


class WilmotPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        councillors = page.xpath('//table[@class="icrtAccordion"]//tr')
        assert len(councillors), "No councillors found"
        for i in range(0, len(councillors), 2):
            role_name, contact_info = councillors[i], councillors[i + 1]
            role, name = role_name.text_content().strip().replace("\xa0", " ").split("— ")

            if "Executive Officer to the Mayor and Council" in role:
                continue

            # "Ward 1 Councillor"
            if "Councillor" in role:
                district = role.split(" Councillor")[0]
                role = "Councillor"
            # "Mayor", "Executive Officer to the Mayor and Council"
            else:
                district = "Wilmot"

            phone = self.get_phone(contact_info)
            email = self.get_email(contact_info)
            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)
            p.add_contact("voice", phone, "legislature")
            p.add_contact("email", email)
            yield p
