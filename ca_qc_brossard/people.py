import re

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.brossard.ca/elus-municipaux"


class BrossardPersonScraper(CanadianScraper):
    def scrape(self):
        secteurs_to_districts = {
            "secteurs c-e-b": "District 1",
            "secteur b": "District 2",
            "secteur a": "District 3",
            "secteurs p-v": "District 4",
            "secteurs t-s-p": "District 5",
            "secteur s": "District 6",
            "secteur r": "District 7",
            "secteurs o-n-i": "District 8",
            "secteurs l-n-j-x-y": "District 9",
            "secteurs l-m-n": "District 1",
        }
        page = self.lxmlize(COUNCIL_PAGE)

        yield self.scrape_mayor(page)

        councillors = page.xpath('//div[@id="ListPosts"]//div[@class="members-post-item"]')

        assert len(councillors), "No councillors found"

        # There is a duplicate of one of the councillors
        names = set()
        for councillor in councillors:
            info_div = councillor.xpath('.//div[@class="members-post-item-content"]')[0]
            name = info_div.xpath(".//a")[0].text_content()
            if name == "Poste vacant" or name in names:
                continue
            names.add(name)

            secteur = info_div.xpath(".//p")[0].text_content()
            # Do some initial cleaning for more robust matching
            secteur = re.sub(r"[–—]", "-", secteur.casefold().replace("sector", "secteur"))
            district = secteurs_to_districts[secteur]
            role = "Conseiller"

            photo = councillor.xpath(".//img/@src")[0]

            p = Person(primary_org="legislature", name=name, district=district, role=role, image=photo)
            p.add_source(COUNCIL_PAGE)

            email_node = councillor.xpath('.//a[@class="members-email"]/@href')
            if email_node:
                email = self.get_email(councillor)
                p.add_contact("email", email)

            phone = self.get_phone(councillor)
            p.add_contact("voice", phone, "legislature")

            yield p

    def scrape_mayor(self, page):
        mayor_div = page.xpath('//div[@class="members-cards"]/div[@class="row"]')[0]
        name = mayor_div.xpath(".//h1")[0].text_content()
        role = "Maire"
        district = "Brossard"
        image = mayor_div.xpath(".//img/@src")[0]

        p = Person(primary_org="legislature", name=name, district=district, role=role, image=image)
        email = self.get_email(mayor_div)
        p.add_contact("email", email)

        phone = self.get_phone(mayor_div)
        p.add_contact("voice", phone, "legislature")
        p.add_source(COUNCIL_PAGE)

        return p
