import re

from pupa.scrape import Organization

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "http://web5.gov.mb.ca/Public/municipalities.aspx"


class ManitobaMunicipalitiesPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        districts = page.xpath('//div[@id="ctl00_PublicContent_divSearchContent"]//tr')[5::3]
        for district in districts:
            title = district.xpath(".//td//text()")
            title = title[0] if len(title[0]) > 1 else "".join(title[:2])

            # @todo Need to distinguish between, e.g., R.M. and Town
            title = title.title()
            organization = Organization(
                name=title + " Municipal Council",
                classification="legislature",
                jurisdiction_id=self.jurisdiction.jurisdiction_id,
            )
            organization.add_source(COUNCIL_PAGE)
            yield organization

            contact = district.xpath(".//td/text()")
            address = " ".join(contact[:4])
            address = re.sub(r"(Fax:.*)", "", address).strip()
            contact = [x for x in contact if "Fax" in x]
            fax = contact[0].split(":")[1].strip()

            phone = district.xpath('.//b[contains(text(), "Phone")]/text()')[0].split(":")[1].strip()
            email = self.get_email(district)

            councillors = district.xpath(".//td[3]/text()")
            positions = district.xpath(".//td[2]/b/text()")
            for i, councillor in enumerate(councillors):
                p = Person(primary_org="legislature", name=councillor, district=title)
                p.add_source(COUNCIL_PAGE)

                if i >= 2:
                    membership = p.add_membership(organization, role="Councillor")
                else:
                    membership = p.add_membership(
                        organization, role=positions[i]
                    )  # @todo "Resident Administrator & Chief Administrative Officer" is split on two lines

                membership.post_id = title
                membership.add_contact_detail("address", address, "legislature")
                membership.add_contact_detail("fax", fax, "legislature")
                membership.add_contact_detail("voice", phone, "legislature")
                membership.add_contact_detail("email", email)
                yield p
