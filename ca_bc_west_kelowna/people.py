import re

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_URL = "https://www.westkelownacity.ca/city-hall/mayor-and-council/contact-mayor-and-council/"


class WestKelownaPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_URL)
        h4_nodes = page.xpath('//h4[contains(., "Contact Mayor") or contains(., "Contact Councillor")]')
        assert h4_nodes, "No council member headings found"
        seat = 0
        for h4 in h4_nodes:
            header = h4.text_content().strip()
            if "Contact Mayor" in header:
                role, district = "Mayor", "West Kelowna"
            else:
                seat += 1
                role, district = "Councillor", f"West Kelowna (seat {seat})"
            container = h4.getparent()
            # Try to find full name in sibling h3 or parent container
            name_el = container.xpath(".//h3")
            if not name_el and container.getparent() is not None:
                name_el = container.getparent().xpath(".//h3")
            email_a = container.xpath('.//a[starts-with(@href,"mailto:")]')
            if not email_a and container.getparent() is not None:
                email_a = container.getparent().xpath('.//a[starts-with(@href,"mailto:")]')
            email = email_a[0].get("href").replace("mailto:", "") if email_a else None
            header_name = re.sub(r"^Contact (?:Mayor|Councillor)\s+", "", header).strip()
            email_name = None
            if email and "mayorandcouncil" not in email:
                first_name = re.split(r"[\._]", email.split("@")[0], maxsplit=1)[0].capitalize()
                if header_name:
                    email_name = f"{first_name} {header_name}"
                else:
                    email_name = " ".join(w.capitalize() for w in re.split(r"[\._]", email.split("@")[0]))
            # Full name from first bio paragraph: "Gord Milsom was elected..." -> "Gord Milsom"
            bio_texts = []
            for search_el in [container, container.getparent()]:
                if search_el is None:
                    continue
                bio_texts = search_el.xpath(".//p//text()")
                if bio_texts:
                    break
            first_sent = " ".join(t.strip() for t in bio_texts if t.strip()).split(".")[0]
            bio_m = re.match(r"^(.+?)\s+(?:was|has|is|served)\b", first_sent)
            if email_name:
                name = email_name
            elif bio_m:
                name = bio_m.group(1).strip()
            elif name_el:
                name = name_el[0].text_content().strip()
            else:
                name = header_name
            phone_li_texts = container.xpath(".//li//text()")
            if container.getparent() is not None:
                phone_li_texts += container.getparent().xpath(".//li//text()")
            phone = None
            for t in phone_li_texts:
                m = re.search(r"\d{3}[-.\s]\d{3}[-.\s]\d{4}", t)
                if m:
                    phone = m.group(0)
                    break
            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_URL)
            if email:
                p.add_contact("email", email)
            if phone:
                p.add_contact("voice", phone, "legislature")
            yield p
