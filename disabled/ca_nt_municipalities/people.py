from pupa.scrape import Organization

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "http://www.nwtac.com/about/communities/"


class NorthwestTerritoriesMunicipalitiesPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        councillors = page.xpath('//div[@class="entry-content"]//p/strong')
        for councillor in councillors:
            district = (
                councillor.xpath("./ancestor::p/preceding-sibling::h2")[-1]
                .text_content()
                .split("–".decode("utf-8"))[0]
            )
            name = " ".join(councillor.text_content().split()[-2:]).replace("-Â".decode("utf-8"), "")
            role = councillor.text_content().replace(name, "").split("-")[0]
            if "SAO" in role or not role:
                continue

            org = Organization(
                name=district + " Municipal Council",
                classification="legislature",
                jurisdiction_id=self.jurisdiction.jurisdiction_id,
            )
            org.add_source(COUNCIL_PAGE)
            yield org

            p = Person(primary_org="legislature", name=name, district=district)
            p.add_source(COUNCIL_PAGE)
            membership = p.add_membership(org, role=role, district=district)

            info = councillor.xpath("./ancestor::p/text()")
            for contact in info:
                if "NT" in contact:
                    membership.add_contact_detail("address", contact.strip(), "legislature")
                if "Tel" in contact:
                    contact = contact.replace("Tel. ", "").replace("(", "").replace(") ", "-").strip()
                    membership.add_contact_detail("voice", contact, "legislature")
                if "Fax" in contact:
                    contact = contact.replace("Fax ", "").replace("(", "").replace(") ", "-").strip()
                    membership.add_contact_detail("fax", contact, "legislature")
            email = self.get_email(councillor, "./parent::p")
            membership.add_contact_detail("email", email)

            if "Website" in councillor.xpath("./parent::p")[0].text_content():
                p.add_link(councillor.xpath("./parent::p//a")[1].attrib["href"])
            yield p
