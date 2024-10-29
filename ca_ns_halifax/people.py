import re

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.halifax.ca/city-hall/districts-councillors"


class HalifaxPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE, user_agent="Mozilla/5.0")
        councillors = page.xpath('//div[@id = "block-districtdistrictindex"]//ul/li')

        assert len(councillors), "No councillors found"
        for councillor in councillors:
            photo_div = councillor.xpath("./a/div[1]")[0]
            info_div = councillor.xpath("./a/div[2]")[0]
            district = re.sub(r"\s*[–—-]\s*", "—", "—".join(info_div.xpath("./p/text()")))
            # District name different than in database
            if "Westphal" in district:
                district = "Cole Harbour—Westphal"

            name = info_div.xpath("./strong/p/text()")[0].replace("Councillor ", "").replace("Deputy Mayor ", "")

            if "Mayor" in name:
                role = "Mayor"
                name = name.replace("Mayor ", "")
                district = "Halifax"
            else:
                role = "Councillor"

            if name != "To be determined":
                photo = photo_div.xpath(".//img/@src")[0]
                url = councillor.xpath("./a/@href")[0]
                councillor_page = self.lxmlize(url, user_agent="Mozilla/5.0")

                phone = self.get_phone(councillor_page, area_codes=[902])
                email = self.get_email(councillor_page)

                p = Person(primary_org="legislature", name=name, district=district, role=role)
                p.add_source(COUNCIL_PAGE)
                p.add_source(url)
                p.add_contact("voice", phone, "legislature")
                p.add_contact("email", email)
                p.image = photo
                yield p
