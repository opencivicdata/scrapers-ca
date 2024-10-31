from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://guelph.ca/city-hall/mayor-and-council/city-council/"
MAYOR_PAGE = "https://guelph.ca/city-hall/mayor-and-council/mayors-office/"


class GuelphPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        councillor_nodes = page.xpath('.//div[@class="thumbnail"]')[1:]
        assert len(councillor_nodes), "No councillors found"

        for councillor_node in councillor_nodes:
            ward_district = councillor_node.xpath(".//h2/text()")[0].split(" Councillors")[0]
            district = ward_district.split(" ")[-1]

            councillors = councillor_node.xpath(".//div/div")
            for councillor in councillors:
                role_and_name = councillor.xpath(".//h3/text()")
                if not role_and_name:
                    continue

                role_and_name = councillor.xpath(".//h3/text()")[0]
                name, role = role_and_name.split(" ", 1)
                contact_info = councillor.xpath(".//p/text()")
                phone = contact_info[1].strip()
                email = self.get_email(councillor)
                if councillor.xpath(".//p/img/@src"):
                    image = councillor.xpath(".//p/img/@src")[0]
                else:
                    image = councillor.xpath(".//div/img/@src")[0]

                p = Person(primary_org="legislature", name=name, district=district, role=role, image=image)
                p.add_contact("email", email)
                if phone:
                    p.add_contact("voice", phone, "legislature")
                p.add_source(COUNCIL_PAGE)

        yield self.scrape_mayor(MAYOR_PAGE)

    def scrape_mayor(self, url):
        page = self.lxmlize(url)

        mayor_node = page.xpath('.//div[@class="entry-content"]/p')[-1]
        name = mayor_node.xpath(".//text()")[0].strip().split("Mayor ")[1]
        phone = self.get_phone(mayor_node)
        email = self.get_email(mayor_node)
        image = mayor_node.xpath('//img[contains(@alt, "Mayor")]/@src')[0]

        p = Person(primary_org="legislature", name=name, district="Guelph", role="Mayor", image=image)
        p.add_contact("voice", phone, "legislature")
        p.add_contact("email", email)
        p.add_source(MAYOR_PAGE)

        return p
