from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.brossard.ca/elus-municipaux"


class BrossardPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        councillors = page.xpath('//div[@id="ListPosts"]//div[@class="members-post-item"]')

        assert len(councillors), "No councillors found"
        for councillor in councillors:
            info_div = councillor.xpath('.//div[@class="members-post-item-content"]')[0]
            name = info_div.xpath(".//a")[0].text_content()
            if name == "Poste vacant":
                continue

            district = info_div.xpath(".//p")[0].text_content()
            role = "Conseiller"

            # district = 'Brossard'
            # role = 'Maire'

            photo = councillor.xpath(".//img/@data-breeze")[0]

            p = Person(primary_org="legislature", name=name, district=district, role=role, image=photo)
            p.add_source(COUNCIL_PAGE)

            email_node = councillor.xpath('.//a[@class="members-email"]/@href')
            if email_node:
                email = self.get_email(councillor)
                p.add_contact("email", email)

            phone = self.get_phone(councillor)
            p.add_contact("voice", phone, "legislature")

            yield p
