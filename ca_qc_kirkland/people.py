import re

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "http://www.ville.kirkland.qc.ca/portrait-municipal/conseil-municipal/elus-municipaux"


class KirklandPersonScraper(CanadianScraper):
    def scrape(self):
        def decode_email(e):
            de = ""
            k = int(e[:2], 16)

            for i in range(2, len(e) - 1, 2):
                de += chr(int(e[i : i + 2], 16) ^ k)

            return de

        page = self.lxmlize(COUNCIL_PAGE)

        councillors = page.xpath('//div[@class="container_content"]//tbody/tr')
        assert len(councillors), "No councillors found"
        for councillor in councillors:
            if councillor == councillors[0]:
                district = "Kirkland"
                role = "Maire"
            else:
                district = councillor.xpath(".//h2")[0].text_content()
                district = re.search(r"District \d", district).group(0)
                role = "Conseiller"

            name = councillor.xpath(".//strong/text()")[0]

            phone = (
                councillor.xpath('.//div[contains(text(), "#")]/text()')[0]
                .replace("T ", "")
                .replace(" ", "-")
                .replace(".", ",")  # correcting a typo
                .replace(",-#-", " x")
            )
            encrypted_email = councillor.xpath('.//@href[contains(., "email")]')[0].split("#")[1]
            email = decode_email(encrypted_email)

            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)
            p.add_contact("voice", phone, "legislature")
            p.add_contact("email", email)
            image = councillor.xpath(".//img/@src")
            if image:
                p.image = image[0]
            yield p
