from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.haldimandcounty.ca/government-administration/council/council-members/"


class HaldimandCountyPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        councillors = page.xpath('//div[contains(@class, "content-col")]//div[contains(@class, "info")]//h3')
        assert len(councillors), "No councillors found"
        for councillor in councillors:
            district_role, name = councillor.text_content().split(" - ")
            if "Mayor" in district_role:
                district = "Haldimand County"
                role = "Mayor"
            else:
                district = district_role.replace("Councillor", "").strip()
                role = "Councillor"

            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)

            info_section = councillor.xpath("./ancestor::section/following-sibling::section")[0]
            p.image = info_section.xpath(".//img/@src")[0]
            email = self.get_email(info_section)
            phone = self.get_phone(info_section)
            p.add_contact("email", email)
            p.add_contact("voice", phone, "legislature")

            yield p
