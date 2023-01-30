# coding: utf-8
import re

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.halifax.ca/city-hall/districts-councillors"
MAYOR_PAGE = "https://www.halifax.ca/city-hall/mayor-mike-savage"
MAYOR_CONTACT_URL = "http://www.halifax.ca/mayor/contact.php"


class HalifaxPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)
        councillors = page.xpath('//div[@id = "block-districtdistrictindex"]/ul/li')[1:]

        assert len(councillors), "No councillors found"
        for councillor in councillors:
            photo_div = councillor.xpath("./a/div[1]")[0]
            info_div = councillor.xpath("./a/div[2]")[0]
            district = re.sub(r"\s*[–—-]\s*", "—", "—".join(info_div.xpath("./p/text()")))
            # FIXME: we special-case one malformed district name. If you're editing this file,
            # try removing these lines
            if district.startswith("District 16 "):
                district = district[len("District 16 ") :]

            name = info_div.xpath("./strong/p/text()")[0].replace("Councillor ", "").replace("Deputy Mayor ", "")

            if name != "To be determined":
                photo = photo_div.xpath(".//img/@src")[0]
                url = councillor.xpath("./a/@href")[0]
                councillor_page = self.lxmlize(url)

                contact_node = councillor_page.xpath('//div[@id = "block-districtdistrictprofile"]')[0]
                phone = self.get_phone(contact_node, area_codes=[902])
                email = self.get_email(contact_node)

                p = Person(primary_org="legislature", name=name, district=district, role="Councillor")
                p.add_source(COUNCIL_PAGE)
                p.add_source(url)
                p.add_contact("voice", phone, "legislature")
                p.add_contact("email", email)
                p.image = photo
                yield p

        mayor_page = self.lxmlize(MAYOR_PAGE, "iso-8859-1")
        name = " ".join(mayor_page.xpath("//h1/text()")).replace("Mayor", "").strip()
        contact_div = mayor_page.xpath('//aside[contains(@class, "layout-sidebar-second")]/section/div[1]')[0]
        phone = self.get_phone(contact_div.xpath("./p[2]")[0])
        email = self.get_email(contact_div.xpath("./p[2]")[0])

        p = Person(primary_org="legislature", name=name, district="Halifax", role="Mayor")
        p.add_source(MAYOR_PAGE)
        p.add_contact("email", email)
        p.add_contact("voice", phone, "legislature")
        yield p
