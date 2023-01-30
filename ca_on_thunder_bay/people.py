from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.thunderbay.ca/en/city-hall/mayor-and-council.aspx"


class ThunderBayPersonScraper(CanadianScraper):
    def scrape(self):
        seat_number = 1
        page = self.lxmlize(COUNCIL_PAGE)

        councillors = page.xpath('//table[@class="icrtAccordion"]//tr[position() mod 2=0]/td')
        assert len(councillors), "No councillors found"
        for councillor in councillors:
            paras = councillor.xpath("./p")
            email = next(para for para in paras if "Email" in para.text_content())
            paras = paras[: paras.index(email)]

            role, name = paras[1].text_content().split(" ", 1)
            district = paras[2].text_content()
            start = 2
            if "At Large" in district:
                role = "Councillor at Large"
                district = "Thunder Bay (seat {})".format(seat_number)
                seat_number += 1
            elif "Ward" in district:
                district = district.replace("Ward", "").strip()
            else:
                district = "Thunder Bay"
                start = 1

            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)

            p.image = paras[0].xpath(".//@src")[0]

            address_parts = []
            for para in paras[start:-1]:
                content = para.text_content().replace("(1st)", "")
                if ":" in content:
                    type, value = content.split(":")
                    if "Fax" in type:
                        p.add_contact("fax", value, "legislature")
                    else:
                        p.add_contact("voice", value, type)
                else:
                    address_parts.append(content)

            p.add_contact("address", "\n".join(address_parts), "constituency")

            yield p
