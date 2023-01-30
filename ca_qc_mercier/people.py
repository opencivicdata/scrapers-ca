import re

from utils import CUSTOM_USER_AGENT
from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "http://www.ville.mercier.qc.ca/02_viedemocratique/default.asp"


class MercierPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE, user_agent=CUSTOM_USER_AGENT, encoding="windows-1252")

        councillors = page.xpath('//table[@width="800"]/tr')
        assert len(councillors), "No councillors found"
        for councillor in councillors:
            if councillor == councillors[0]:
                name = councillor.xpath(".//strong/text()")[0].replace("Monsieur", "").replace("Madame", "").strip()
                role = "Maire"
                district = "Mercier"
            else:
                name = councillor.xpath(".//strong/text()")[0].replace("Monsieur", "").replace("Madame", "").strip()
                role = "Conseiller"
                district = "District {}".format(re.search(r"(\d)", councillor.xpath(".//text()")[3]).group(1))

            email = self.get_email(councillor)

            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)
            p.add_contact("email", email)
            yield p
