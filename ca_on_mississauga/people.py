import re

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "http://www.mississauga.ca/portal/cityhall/mayorandcouncil"
CONTACT_PAGE = "http://www.mississauga.ca/portal/helpfeedback/contactus"


class MississaugaPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        councillors = page.xpath('//li/a[contains(@href, "ward")]')
        assert len(councillors), "No councillors found"
        for councillor_url in councillors:
            if "vacant" not in councillor_url.xpath(".//div//div[1]/text()")[0].lower():
                yield self.councillor_data(councillor_url.attrib["href"])

        mayor_url = page.xpath('//li/a[contains(@href, "mayor")]')[0]
        if "vacant" not in mayor_url.xpath(".//div//div[1]/text()")[0].lower():
            yield self.mayor_data(mayor_url.attrib["href"])

    def councillor_data(self, url):
        page = self.lxmlize(url)

        name_district = page.xpath('//*[@id="com-main"]/div/div/div/h1/text()')[0]
        district, name = re.split(r" – (?:Councillor (?:and Deputy Mayor )?)?", name_district)  # n-dash
        email = self.get_email(page, '//section[contains(@class, "module-content")]')
        photo = page.xpath(
            '//section[contains(@class, "module-content")]/p[1]/img/@src|//section[contains(@class, "module-content")]/p[1]/b/img/@src|//section[contains(@class, "module-content")]/p[1]/strong/img/@src'
        )[0]

        p = Person(primary_org="legislature", name=name, district=district, role="Councillor")
        p.add_source(COUNCIL_PAGE)
        p.add_source(url)
        p.add_contact("email", email)
        p.image = photo

        return p

    def mayor_data(self, url):
        page = self.lxmlize(url)

        name = page.xpath('//*[@id="com-main"]/div/div/div/h1/text()')[0]
        name = name.replace("Mayor – ", "")
        photo = page.xpath('//*[@id="65a01af8598b7"]/p[1]/img/@src')[0]

        p = Person(primary_org="legislature", name=name, district="Mississauga", role="Mayor")
        p.add_source(url)
        p.add_source(CONTACT_PAGE)
        p.add_contact("email", "mayor@mississauga.ca")  # hardcoded
        p.image = photo

        return p
