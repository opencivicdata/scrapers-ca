import requests

from utils import DEFAULT_USER_AGENT, CanadianScraper
from utils import CanadianPerson as Person

COUNCIL_PAGE = "https://www.thunderbay.ca/en/city-hall/mayor-and-council-profiles.aspx"


class ThunderBayPersonScraper(CanadianScraper):
    def scrape(self):
        seat_number = 1
        page = self.lxmlize(COUNCIL_PAGE)

        councillors = page.xpath("//p[@class='Center']/a[@href]")
        assert len(councillors), "No councillors found"
        for councillor in councillors:
            url = councillor.xpath("./@href")[0]
            councillor_page = self.lxmlize(url)
            info = councillor_page.xpath("//div[@class='iCreateDynaToken']")[1]
            role = info.xpath("./h2")[0].text_content()
            name = info.xpath("./h3")[0].text_content()

            email = self.get_email(info)
            phone = self.get_phone(info)
            photo = councillor_page.xpath("//div[@class='lb-imageBoxLinkImage']//img/@src")[0]

            district = councillor_page.xpath("//span[@class='imageBoxSpan']|//div[@class='lb-imageBoxLinkTitle']/h2")[
                0
            ].text_content()
            if "At Large" in district:
                role = "Councillor at Large"
                district = f"Thunder Bay (seat {seat_number})"
                seat_number += 1
            elif "Mayor" in district:
                district = "Thunder Bay"

            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)
            p.add_source(url)
            p.add_contact("email", email)
            p.add_contact("voice", phone, "legislature")
            p.image = photo

            yield p

    def lxmlize(self, url, encoding=None, *, user_agent=DEFAULT_USER_AGENT, cookies=None, xml=False):
        requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ":HIGH:!DH:!aNULL"  # site uses a weak DH key
        return super().lxmlize(url, encoding, user_agent, cookies, xml)
