import re

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.countygp.ab.ca/council-administration/council/"
BASE_URL = "https://www.countygp.ab.ca"


class GrandePrairieCountyNo1PersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)
        councillors = page.xpath(
            '//div[contains(@class,"component-main") and contains(@class,"justify-content-between")'
            ' and .//h3[contains(text(),"Division")]]'
        )

        assert len(councillors), "No councillors found"
        for councillor in councillors:
            district = councillor.xpath('.//h3[contains(text(),"Division")]')[0].text_content().strip()

            email_link = councillor.xpath('.//a[contains(@href,"mailto:")]')
            if not email_link:
                continue
            link_text = email_link[0].text_content().strip()
            # Strip role prefix: "Email Reeve ", "Email Deputy Reeve ", "Email Councillor "
            name = re.sub(r"^Email\s+(Deputy Reeve|Reeve|Councillor)\s+", "", link_text).strip()
            email = email_link[0].get("href", "").replace("mailto:", "")

            p = Person(primary_org="legislature", name=name, district=district, role="Councillor")
            p.add_source(COUNCIL_PAGE)

            if email:
                p.add_contact("email", email)

            img = councillor.xpath(".//img/@src")
            if img:
                src = img[0]
                p.image = src if src.startswith("http") else BASE_URL + src

            yield p
