import re

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "http://www.ville.kirkland.qc.ca/portrait-municipal/conseil-municipal/elus-municipaux"


class KirklandPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        # councillors = page.xpath('//div[@id="PageContent"]/table/tbody/tr/td')
        councillors = page.xpath('//table/tbody[not(@id)]/tr/td[@valign="top"]')
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

            # Using self.get_phone does not include the extension #
            phone = (
                councillor.xpath('.//div[contains(text(), "#")]/text()')[0]
                .replace("T ", "")
                .replace(" ", "-")
                .replace(".", ",")
                .replace(",-#-", " x")
            )
            encrypted_email = councillor.xpath('.//@href[contains(., "email")]')[0].split("#")[1]
            email = decode_email(encrypted_email)

            # cloudflare encrypts the email data
            email = councillor.xpath('.//div/*/*/@href | .//div/*/@href | .//@href')[0]
            decoded_email = decode_email(email.split("#", 1)[1])
            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)
            p.add_contact("voice", phone, "legislature")
            p.add_contact("email", decoded_email)
            image = councillor.xpath(".//img/@src")
            if image:
                p.image = image[0]
            yield p
