from utils import CanadianPerson as Person
from utils import CanadianScraper

MAYOR_URL = "https://www.shawinigan.ca/ville/conseil-municipal/mot-du-maire/"
LISTING_URL = "https://www.shawinigan.ca/ville/conseil-municipal/conseillers-municipaux/"


class ShawiniganPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(MAYOR_URL)
        name_p = page.xpath('//p[contains(., "maire de Shawinigan")]')
        assert name_p, "Mayor name paragraph not found"
        name = name_p[0].text_content().split(",")[0].strip()
        email = self.get_email(page, error=False)
        phone_link = page.xpath('.//a[starts-with(@href,"tel:")]')
        phone = phone_link[0].text_content().strip() if phone_link else None

        p = Person(primary_org="legislature", name=name, district="Shawinigan", role="Mayor")
        p.add_source(MAYOR_URL)
        if email:
            p.add_contact("email", email)
        if phone:
            p.add_contact("voice", phone, "legislature")
        yield p

        listing = self.lxmlize(LISTING_URL)
        district_urls = list(
            dict.fromkeys(listing.xpath("//a[contains(@href, '/conseillers-municipaux/district')]/@href"))
        )
        assert district_urls, "No district URLs found"

        for url in district_urls:
            dpage = self.lxmlize(url)
            h1s = dpage.xpath("//h1")
            if not h1s:
                continue
            district = h1s[0].text_content().strip()

            contact_ps = dpage.xpath(
                '//p[a[starts-with(@href,"mailto:") and contains(@href,"@shawinigan.ca")'
                ' and not(contains(@href,"information@"))]]'
            )
            if not contact_ps:
                continue

            name_p = contact_ps[0].xpath("preceding-sibling::p[1]")
            if not name_p:
                continue
            name = name_p[0].text_content().strip()
            if not name:
                continue

            email = contact_ps[0].xpath("a/@href")[0].replace("mailto:", "")
            phone_link = dpage.xpath('.//a[starts-with(@href,"tel:")]')
            phone = phone_link[0].text_content().strip() if phone_link else None
            image = dpage.xpath('//article//img[not(contains(@src,"logo"))]/@src')

            p = Person(primary_org="legislature", name=name, district=district, role="Councillor")
            p.add_source(LISTING_URL)
            p.add_source(url)
            p.add_contact("email", email)
            if phone:
                p.add_contact("voice", phone, "legislature")
            if image:
                p.image = image[0]
            yield p
