import re

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.ville.sainte-anne-de-bellevue.qc.ca/fr/199/elus-municipaux"


class SainteAnneDeBellevuePersonScraper(CanadianScraper):
    def scrape(self):
        def decode_email(e):
            de = ""
            k = int(e[:2], 16)

            for i in range(2, len(e) - 1, 2):
                de += chr(int(e[i : i + 2], 16) ^ k)

            return de

        page = self.lxmlize(COUNCIL_PAGE)

        councillors = page.xpath('//div[@class="block text"]')
        assert len(councillors), "No councillors found"
        for councillor in councillors:
            name = councillor.xpath('.//div[@class="content-writable"]//strong/text()')[0]
            district = councillor.xpath(".//h2/text()")[0]

            if "Maire" in district:
                district = "Sainte-Anne-de-Bellevue"
                role = "Maire"
            else:
                district = "District {}".format(re.search(r"\d+", district)[0])
                role = "Conseiller"

            encoded_email = councillor.xpath('.//@href[contains(., "email-protection")]')[0].split("#")[1]

            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)

            p.image = councillor.xpath(".//@src")[0]
            p.add_contact("email", decode_email(encoded_email))
            yield p
