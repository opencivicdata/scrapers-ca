from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.surrey.ca/city-government/mayor-council/city-councillors"


class SurreyPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)
        members = page.xpath("//article[@class='teaser']")

        assert len(members), "No members found"
        seat_number = 1
        for member in members:
            role, name = member.xpath('.//a[@class="teaser__link"]/h4')[0].text_content().split(" ", 1)
            district = f"Surrey (seat {seat_number})"
            seat_number += 1
            photo_url = member.xpath(".//figure//img/@src")[0]

            url = member.xpath('.//a[@class="teaser__link"]/@href')[0]
            ext_infos = self.scrape_extended_info(url)
            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)
            p.add_source(url)
            p.image = photo_url

            if ext_infos:  # member pages might return errors
                email, phone = ext_infos
                if email:
                    p.add_contact("email", email)
                if phone:
                    p.add_contact("voice", phone, "legislature")
            yield p

        mayor_url = page.xpath('//nav[@id="content-nav"]//a[contains(., "Mayor")]/@href')[0]

        page = self.lxmlize(mayor_url)
        role, name = page.xpath("//h1/span")[0].text_content().split(" ", 1)
        ext_infos = self.scrape_extended_info(mayor_url)
        photo_url = page.xpath('//div[@class="page-header__hero js-cover-image"]/img/@src')[0]

        p = Person(primary_org="legislature", name=name, district="Surrey", role=role)
        p.add_source(mayor_url)
        p.image = photo_url

        if ext_infos:  # member pages might return errors
            email, phone = ext_infos
            if email:
                p.add_contact("email", email)
            if phone:
                p.add_contact("voice", phone, "legislature")
        yield p

    def scrape_extended_info(self, url):
        phone = None
        email = None
        root = self.lxmlize(url)
        email = self.get_email(root)
        phone = self.get_phone(root)
        return email, phone
