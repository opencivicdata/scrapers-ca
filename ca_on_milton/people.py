from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.milton.ca/en/town-hall/councillors.aspx"
MAYOR_PAGE = "https://www.milton.ca/en/town-hall/mayor-of-milton.aspx"


class MiltonPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        wards = page.xpath('//div[@class="fbg-col-xs-12 fbg-col-sm-4 column lmColumn ui-sortable"]//a')[1:5]
        assert len(wards), "No wards found"
        for ward in wards:
            district = ward.text_content()
            url = ward.xpath("./@href")[0]
            page = self.lxmlize(url)
            councillors = page.xpath('//div[@class="fbg-col-xs-12"]')[1:]
            assert len(councillors), "No councillors found"
            for councillor in councillors:
                p = self.scrape_person(councillor, district, url)
                if p is not None:
                    yield p

        page = self.lxmlize(MAYOR_PAGE)
        info = page.xpath('//div[@class="fbg-col-xs-12"]')[0]
        yield self.scrape_person(info, "Milton", MAYOR_PAGE)

    def scrape_person(self, node, district, source):
        role, name = node.xpath(".//h2/text()")[:2]
        if "Vacant" in name:
            return None
        role = role.strip()
        if role == "Town Councillor":
            role = "Councillor"
        email_node = node.xpath('.//a/@href[contains(., "mailto")]')
        if email_node:
            email = self.get_email(node)
        p = Person(primary_org="legislature", name=name, district=district, role=role)
        p.add_source(source)
        if role != "Mayor":
            p.add_source(COUNCIL_PAGE)
            phone = self.get_phone(node)
        else:
            phone = p.clean_telephone_number(node.xpath('.//a[contains(./@href, "tel")]')[0].text_content())
        p.image = node.xpath(".//img/@src")[0]
        if email_node:
            p.add_contact("email", email)
        p.add_contact("voice", phone, "legislature")

        return p
