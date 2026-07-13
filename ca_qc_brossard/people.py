import re

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.brossard.ca/elus-municipaux"


class BrossardPersonScraper(CanadianScraper):
    def scrape(self):
        secteurs_to_districts = {
            "c, e, l": "District 1",
            "c, b": "District 2",
            "b": "District 3",
            "a": "District 4",
            "p, v": "District 5",
            "t, p": "District 6",
            "r, s": "District 7",
            "r": "District 8",
            "o, n, i": "District 9",
            "l, j, x, y": "District 10",
            "m, n": "District 11",
            "secteur saint-laurent": "District 12",
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

            photo = councillor.xpath('.//img[not(starts-with(@src, "data:"))]/@src')
            photo = photo[0] if photo else None

            p = Person(primary_org="legislature", name=name, district=district, role=role, image=photo)
            p.add_source(COUNCIL_PAGE)

            email_node = councillor.xpath('.//a[@class="members-email"]/@href')
            if email_node:
                email = self.get_email(councillor)
                p.add_contact("email", email)

            phone = self.get_phone(councillor, error=False)
            if phone:
                p.add_contact("voice", phone, "legislature")

            yield p

    def scrape_mayor(self, page):
        mayor_div = page.xpath('//div[@class="members-cards"]/div[@class="row"]')[0]
        name = mayor_div.xpath(".//h1")[0].text_content()
        role = "Maire"
        district = "Brossard"
        image = mayor_div.xpath('.//img[not(starts-with(@src, "data:"))]/@src')
        image = image[0] if image else None

        p = Person(primary_org="legislature", name=name, district=district, role=role, image=image)
        email = self.get_email(mayor_div, error=False)
        if email:
            p.add_contact("email", email)

        phone = self.get_phone(mayor_div, error=False)
        if phone:
            p.add_contact("voice", phone, "legislature")
        p.add_source(COUNCIL_PAGE)

        return p
