import json
import re

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.oshawa.ca/en/city-hall/council-members.aspx"


class OshawaPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)
        councillors = page.xpath("//div[@class='fbg-row lb-callToAction cm-datacontainer']")

        assert len(councillors), "No councillors found"
        for councillor in councillors:
            info = councillor.xpath(".//div[@class='lb-callToAction_header']")[0].text_content()
            if "Mayor" in info:
                role = "Mayor"
                district = "Oshawa"
                name = info.replace("Mayor ", "")
            else:
                district, role_name = re.split(r"(?<=\d)\s", info, maxsplit=1)
                role = "Regional Councillor" if "Regional" in role_name else "Councillor"
                name = re.split(r"Councillor\s", role_name, maxsplit=1)[1]

            photo_url = councillor.xpath(".//img/@src")[0]
            phone = self.get_phone(councillor)
            links = councillor.xpath(".//a/@href")
            data = json.loads(councillor.xpath("./@data-cm-itemdata")[0])
            email = data["items"][0]["linkUrl"].replace("mailto:", "")

            p = Person(primary_org="legislature", name=name, district=district, role=role, image=photo_url)
            p.add_source(COUNCIL_PAGE)
            p.add_contact("voice", phone, "legislature")
            p.add_contact("email", email)
            for link in links:
                if "mail" not in link:
                    p.add_link(link)
            yield p
