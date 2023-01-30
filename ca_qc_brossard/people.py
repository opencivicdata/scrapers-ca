import re

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "http://www.ville.brossard.qc.ca/Ma-ville/conseil-municipal/Municipal-council.aspx?lang=en-ca"
CONTACT_PAGE = "http://www.ville.brossard.qc.ca/Ma-ville/conseil-municipal/Municipal-council/Municipal-council-members-%E2%80%93-Contact-information.aspx"


class BrossardPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)
        contact_page = self.lxmlize(CONTACT_PAGE)

        councillors = page.xpath('//a[contains(@class, "slide item-")]')
        emails = contact_page.xpath('//a[contains(@href, "mailto:")]')

        assert len(councillors), "No councillors found"
        for councillor in councillors:
            name = councillor.xpath('.//div[@class="titre"]/text()')[0]
            if name == "Poste vacant":
                continue
            if name == "Sylvie Desgroseilliers":
                name = "Sylvie DesGroseilliers"

            position = councillor.xpath('.//div[@class="poste"]/text()')[0]
            role = "Conseiller"

            district = re.search(r"District \d+", position)
            if "Mayor" in position:
                district = "Brossard"
                role = "Maire"
            else:
                district = district.group(0)

            photo = re.search(r"url\((.+)\)", councillor.attrib["style"]).group(1)

            p = Person(primary_org="legislature", name=name, district=district, role=role, image=photo)
            p.add_source(COUNCIL_PAGE)
            p.add_source(CONTACT_PAGE)

            index = [i for i, link in enumerate(emails) if name in link.text_content().replace("\u2019", "'")][0]
            email = emails[index + 1]
            p.add_contact("email", re.match("mailto:(.+@brossard.ca)", email.attrib["href"]).group(1))
            phone = email.xpath('./preceding-sibling::text()[contains(., "450")]')
            phone = phone[-1]
            p.add_contact("voice", phone, "legislature")

            yield p
