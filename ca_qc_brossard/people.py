from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.brossard.ca/elus-municipaux"


class BrossardPersonScraper(CanadianScraper):
    def scrape(self):
        secteurs_to_districts = {
            "Secteurs C-E-B": "District 1",
            "Secteur B": "District 2",
            "Secteur A": "District 3",
            "Secteurs P-V": "District 4",
            "Secteurs T-S-P": "District 5",
            "Secteur S": "District 6",
            "Secteur R": "District 7",
            "Secteurs O-N-I": "District 8",
            "Secteurs L-N-J-X-Y": "District 9",
            "Secteurs L-M-N": "District 1",
        }
        page = self.lxmlize(COUNCIL_PAGE)

        councillors = page.xpath('//div[@id="ListPosts"]//div[@class="members-post-item"]')

        assert len(councillors), "No councillors found"
        for councillor in councillors:
            info_div = councillor.xpath('.//div[@class="members-post-item-content"]')[0]
            name = info_div.xpath(".//a")[0].text_content()
            if name == "Poste vacant":
                continue

            secteur = info_div.xpath(".//p")[0].text_content()
            district = secteurs_to_districts[secteur]
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
