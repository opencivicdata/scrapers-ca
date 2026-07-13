import re

from utils import CanadianPerson as Person
from utils import CanadianScraper

LISTING_URL = "https://ville.valleyfield.qc.ca/conseil-municipal/"
BASE = "https://ville.valleyfield.qc.ca"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/125 Safari/537.36"


class SalaberryDeValleyfieldPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(LISTING_URL, user_agent=USER_AGENT)
        profile_links = list(dict.fromkeys(page.xpath('//h3/a[contains(@href,"/conseil-municipal/")]/@href')))
        assert profile_links, "No member profile links found"
        seat = 0
        for href in profile_links:
            url = BASE + href if not href.startswith("http") else href
            ppage = self.lxmlize(url, user_agent=USER_AGENT)
            name = ppage.xpath("//h1")[0].text_content().strip() if ppage.xpath("//h1") else ""
            if not name:
                continue
            body = ppage.xpath("//body")[0]
            role_els = body.xpath('.//*[contains(text(),"Maire") or contains(text(),"Conseiller")]')
            role_text = role_els[0].text_content() if role_els else ""
            if "Maire" in role_text and "Conseiller" not in role_text:
                role, district = "Mayor", "Salaberry-de-Valleyfield"
            else:
                m = re.search(r"district[- ]?(\d+)", url + " " + body.text_content(), re.I)
                if m:
                    num = int(m.group(1))
                else:
                    seat += 1
                    num = seat
                role, district = "Councillor", f"District {num}"
            email_el = ppage.xpath('.//a[starts-with(@href,"mailto:")]')
            email = email_el[0].get("href").replace("mailto:", "") if email_el else None
            phone_link = ppage.xpath('.//a[starts-with(@href,"tel:")]')
            phone = phone_link[0].text_content().strip() if phone_link else None
            image = ppage.xpath('//img[contains(@src,"/media/") or contains(@src,"conseil")]/@src')
            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(LISTING_URL)
            p.add_source(url)
            if email:
                p.add_contact("email", email)
            if phone:
                p.add_contact("voice", phone, "legislature")
            if image:
                p.image = image[0]
            yield p
