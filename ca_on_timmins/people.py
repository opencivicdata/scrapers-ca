import re

from utils import CanadianPerson as Person
from utils import CanadianScraper

LISTING_URL = "https://www.timmins.ca/how_do_i_/contact_an_elected_official"
MAYOR_URL = "https://www.timmins.ca/our_services/city_hall/mayor_and_council/mayors_office/"
BASE = "https://www.timmins.ca"
BROWSER_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36"
)


class TimminsPersonScraper(CanadianScraper):
    def scrape(self):
        # Mayor is not on the contact listing page — fetch separately
        mpage = self.lxmlize(MAYOR_URL, user_agent=BROWSER_USER_AGENT)
        name_h = mpage.xpath("//h1")
        mayor_name = name_h[0].text_content().strip() if name_h else ""
        if not mayor_name or "Mayor" in mayor_name:
            text = " ".join(mpage.xpath("//body//text()"))
            m = re.search(r"Mayor\s+([A-Z][A-Za-z' -]+)", text)
            mayor_name = m.group(1).strip() if m else ""
        assert mayor_name, "Mayor name not found"
        mayor_email = self.get_email(mpage, error=False)
        mayor_phone = self.get_phone(mpage, area_codes=[705], error=False)
        mayor_image = mpage.xpath('//img[contains(@src,"civiclive.com")]/@src')
        p = Person(primary_org="legislature", name=mayor_name, district="Timmins", role="Mayor")
        p.add_source(MAYOR_URL)
        if mayor_email:
            p.add_contact("email", mayor_email)
        if mayor_phone:
            p.add_contact("voice", mayor_phone, "legislature")
        if mayor_image:
            p.image = mayor_image[0]
        yield p

        # Councillors — filter to pageIds >= 19111000 to exclude nav links
        page = self.lxmlize(LISTING_URL, user_agent=BROWSER_USER_AGENT)
        all_links = page.xpath('//a[contains(@href,"portalId=11976429")]/@href')
        member_links = list(
            dict.fromkeys(
                h
                for h in all_links
                if re.search(r"pageId=(\d+)", h) and int(re.search(r"pageId=(\d+)", h).group(1)) >= 19111000
            )
        )
        assert member_links, "No councillor CMS links found"
        ward5_seat = 0
        for href in member_links:
            url = href if href.startswith("http") else BASE + href
            ppage = self.lxmlize(url, user_agent=BROWSER_USER_AGENT)
            name_h = ppage.xpath("//h1")
            name = name_h[0].text_content().strip() if name_h else ""
            name = re.sub(r"^Ward\s+\d+\s*[-–]\s*", "", name).strip()
            name = re.sub(r"^Councillor\s+", "", name).strip()
            if not name:
                continue
            body_text = " ".join(ppage.xpath("//body//text()"))
            ward_m = re.search(r"Ward\s+(\d+)", body_text, re.I)
            ward_num = int(ward_m.group(1)) if ward_m else None
            role = "Councillor"
            if ward_num == 5:
                ward5_seat += 1
                district = f"Ward 5 (seat {ward5_seat})"
            elif ward_num:
                district = f"Ward {ward_num}"
            else:
                district = "Timmins"
            email = self.get_email(ppage, error=False)
            phone = self.get_phone(ppage, area_codes=[705], error=False)
            image = ppage.xpath('//img[contains(@src,"civiclive.com")]/@src')
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
