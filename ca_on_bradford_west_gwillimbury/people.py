import re

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_URL = "https://www.townofbwg.com/town-hall/council/council-members/"


class BradfordWestGwillimburyPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_URL)
        member_imgs = page.xpath('//img[contains(@alt,"of BWG")]')
        assert member_imgs, "No council member images found"
        for img in member_imgs:
            alt = img.get("alt", "")
            m = re.search(r"(?:Town of BWG\s+)(.+?),\s+(.+)$", alt)
            if not m:
                continue
            role_str, name = m.group(1).strip(), m.group(2).strip()
            if re.search(r"\bMayor\b", role_str) and "Deputy" not in role_str:
                role, district = "Mayor", "Bradford West Gwillimbury"
            elif "Deputy Mayor" in role_str:
                role, district = "Councillor", "Deputy Mayor"
            else:
                ward_m = re.search(r"War(?:d)?\s+(\d+)", role_str)
                role = "Councillor"
                district = f"Ward {ward_m.group(1)}" if ward_m else role_str
            # Walk up from img to find container with email link
            container = img.getparent()
            email_a = []
            for _ in range(6):
                if container is None:
                    break
                email_a = container.xpath('.//a[starts-with(@href,"mailto:")]')
                if email_a:
                    break
                container = container.getparent()
            email = email_a[0].get("href").replace("mailto:", "") if (container is not None and email_a) else None
            phone_link = container.xpath('.//a[starts-with(@href,"tel:")]') if container is not None else []
            if phone_link:
                phone = phone_link[0].text_content().strip()
            else:
                phone_texts = container.xpath(".//text()") if container is not None else []
                phone = None
                for t in phone_texts:
                    pm = re.search(r"\d{3}[-.\s]\d{3}[-.\s]\d{4}", t)
                    if pm:
                        phone = pm.group(0)
                        break
            image_src = img.get("src", "")
            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_URL)
            if email:
                p.add_contact("email", email)
            if phone:
                p.add_contact("voice", phone, "legislature")
            if image_src:
                p.image = image_src
            yield p
