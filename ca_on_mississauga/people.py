from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "http://www.mississauga.ca/portal/cityhall/mayorandcouncil"
MAYOR_PAGE = "http://www.mississauga.ca/portal/cityhall/mayorsoffice"
CONTACT_PAGE = "http://www.mississauga.ca/portal/helpfeedback/contactus"


class MississaugaPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        councillors = page.xpath('//li/a[contains(@href, "ward")]')
        assert len(councillors), "No councillors found"
        for councillor_url in councillors:
            if "Vacant" not in councillor_url.xpath(".//div//div[1]/text()")[0]:
                yield self.councillor_data(councillor_url.attrib["href"])

        mayor_page = self.lxmlize(MAYOR_PAGE)
        mayor_name = mayor_page.xpath('//*[@id="com-main"]/div/div/div/h1/text()')[0]
        if "vacant" not in mayor_name.lower():
            yield self.mayor_data(MAYOR_PAGE)

    def councillor_data(self, url):
        page = self.lxmlize(url)

        name_district = page.xpath('//*[@id="com-main"]/div/div/div/h1/text()')[0]
        hyphen = name_district.find('Councillor')
        district = name_district[:hyphen -3]
        name = name_district[hyphen:]
        bracket = name.find('(')
        if bracket != -1:
            name = name[:bracket]
        email = self.get_email(page, '//section[contains(@class, "module-content")]')
        photo = page.xpath('//section[contains(@class, "module-content")]/p[1]/img/@src|//section[contains(@class, "module-content")]/p[1]/b/img/@src|//section[contains(@class, "module-content")]/p[1]/strong/img/@src')[0]

        p = Person(primary_org="legislature", name=name, district=district, role="Councillor")
        p.add_source(COUNCIL_PAGE)
        p.add_source(url)
        p.add_contact("email", email)
        p.image = photo

        return p

    def mayor_data(self, url):
        page = self.lxmlize(url)

        name_text = page.xpath('//*[@id="com-main"]/div/div/div/h1/text()')[0]
        name = name_text.split(",")[0]
        photo = page.xpath('//img[contains(@src, "mayor")]/@src')[0]

        p = Person(primary_org="legislature", name=name, district="Mississauga", role="Mayor")
        p.add_source(url)
        p.add_source(CONTACT_PAGE)
        p.add_contact("email", "mayor@mississauga.ca")  # hardcoded
        p.image = photo

        return p
