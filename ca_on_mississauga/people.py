import re

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.mississauga.ca/council/city-council-members/"
CONTACT_PAGE = "https://www.mississauga.ca/council/city-council-members/"


class MississaugaPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        councillors = page.xpath('//a[contains(@href, "ward-") and contains(@href, "councillor")]')
        assert len(councillors), "No councillors found"
        for councillor_url in councillors:
            text = councillor_url.text_content()
            if "vacant" not in text.lower():
                yield self.councillor_data(councillor_url.attrib["href"])

        mayor_url = page.xpath('//a[contains(@href, "mayor")]')
        for url_node in mayor_url:
            href = url_node.attrib["href"]
            if "city-council-members" in href and "vacant" not in url_node.text_content().lower():
                yield self.mayor_data(href)
                break

    def councillor_data(self, url):
        page = self.lxmlize(url)

        name_district = page.xpath("//h1/text()")[0]
        district, name = re.split(r" [–-] (?:Councillor (?:and Deputy Mayor )?)?", name_district)  # n-dash or hyphen
        email = self.get_email(page, error=False)
        photos = page.xpath('//img[contains(@src, "wp-content")]/@src')
        photo = photos[0] if photos else None

        p = Person(primary_org="legislature", name=name, district=district, role="Councillor")
        p.add_source(COUNCIL_PAGE)
        p.add_source(url)
        if email:
            p.add_contact("email", email)
        if photo:
            p.image = photo

        return p

    def mayor_data(self, url):
        page = self.lxmlize(url)

        name = page.xpath("//h1/text()")[0]
        name = re.sub(r"^Mayor\s*[–-]\s*", "", name)
        photos = page.xpath('//img[contains(@src, "wp-content")]/@src')
        photo = photos[0] if photos else None

        p = Person(primary_org="legislature", name=name, district="Mississauga", role="Mayor")
        p.add_source(url)
        p.add_source(CONTACT_PAGE)
        p.add_contact("email", "mayor@mississauga.ca")  # hardcoded
        if photo:
            p.image = photo

        return p
