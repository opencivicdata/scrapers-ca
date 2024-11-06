from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://ville.ddo.qc.ca/en/my-city/council/members-of-council-and-electoral-districts/"


class DollardDesOrmeauxPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)
        general_contacts = page.xpath(
            "//h2/ancestor::div[@class='elementor-widget-wrap elementor-element-populated']"
        )[0]
        general_phone = general_contacts.xpath('.//span[contains(., "phone")]/text()')[0].split(": ")[1]
        general_fax = general_contacts.xpath('.//span[contains(., "fax")]/text()')[0].split(": ")[1]

        councillors = page.xpath('//h3/ancestor::div[@class="elementor-widget-wrap elementor-element-populated"]')[1:]
        assert len(councillors), "No councillors found"
        for councillor in councillors:
            name = councillor.xpath(".//h4/text()")[0]
            name = " ".join(reversed(name.split(", ")))
            district = councillor.xpath(".//h3/text()")[0]
            email = self.get_email(councillor)

            if district == "Mayor":
                district = "Dollard-Des Ormeaux"
                role = "Maire"
            else:
                role = "Conseiller"

            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)
            image = councillor.xpath(".//@data-src")
            if image:
                p.image = image[0]
            p.add_contact("email", email)
            p.add_contact("voice", general_phone, "legislature")
            p.add_contact("fax", general_fax, "legislature")

            yield p
