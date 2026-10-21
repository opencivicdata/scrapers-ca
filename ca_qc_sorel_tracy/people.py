import re

from utils import CanadianPerson as Person
from utils import CanadianScraper

MAYOR_URL = "https://www.ville.sorel-tracy.qc.ca/ville/vos-elus/maire"
COUNCIL_URL = "https://www.ville.sorel-tracy.qc.ca/ville/vos-elus/conseillers-et-conseilleres"


class SorelTracyPersonScraper(CanadianScraper):
    def scrape(self):
        # Mayor — h1 is the page title "Maire", name is in a paragraph
        mpage = self.lxmlize(MAYOR_URL)
        name_p = mpage.xpath('//p[contains(., "maire actuel") or contains(., "mairesse actuelle")]')
        if name_p:
            text = name_p[0].text_content().strip()
            name_m = re.search(r"est M(?:me\.?|\.)\s+(.+?)\.?\s*$", text)
            name = name_m.group(1).strip() if name_m else ""
        else:
            name = ""
        assert name, "Mayor name not found"
        email_a = mpage.xpath('.//a[starts-with(@href,"mailto:")]')
        email = email_a[0].get("href").replace("mailto:", "").split("?", 1)[0] if email_a else None
        phone_link = mpage.xpath('.//a[starts-with(@href,"tel:")]')
        phone = phone_link[0].text_content().strip() if phone_link else None
        p = Person(primary_org="legislature", name=name, district="Sorel-Tracy", role="Mayor")
        p.add_source(MAYOR_URL)
        if email:
            p.add_contact("email", email)
        if phone:
            p.add_contact("voice", phone, "legislature")
        yield p

        # Councillors — page now uses h2 for names (not h4), followed by h3 for district
        cpage = self.lxmlize(COUNCIL_URL)
        h2_nodes = cpage.xpath('//h2[contains(., "M.") or contains(., "Mme")]')
        assert h2_nodes, "No councillor h2 found"
        for h2 in h2_nodes:
            name = re.sub(r"^(M\.|Mme\.?)\s*", "", h2.text_content().strip()).strip()
            if not name:
                continue
            parent = h2.getparent()
            children = list(parent)
            h2_idx = children.index(h2)
            next_h2_idx = next(
                (i for i, el in enumerate(children[h2_idx + 1 :], h2_idx + 1) if el.tag == "h2"),
                len(children),
            )
            member_els = children[h2_idx + 1 : next_h2_idx]
            h3_els = [el for el in member_els if el.tag == "h3"]
            p_els = [el for el in member_els if el.tag == "p"]
            if not h3_els:
                continue
            m = re.search(r"n[°o]?\s*(\d+)", h3_els[0].text_content(), re.I)
            if not m:
                continue
            district = f"District {int(m.group(1))}"
            email = None
            phone = None
            image = []
            for p_el in p_els:
                if not email:
                    a_el = p_el.xpath('.//a[starts-with(@href,"mailto:")]')
                    if a_el:
                        email = a_el[0].get("href").replace("mailto:", "").split("?", 1)[0]
                if not phone:
                    a_el = p_el.xpath('.//a[starts-with(@href,"tel:")]')
                    if a_el:
                        phone = a_el[0].text_content().strip()
                if not image:
                    image = p_el.xpath(".//img/@src")
            if not phone:
                for p_el in p_els[:3]:
                    pm = re.search(r"\b\d{3}[\s.-]\d{3}[-.\s]\d{4}\b", p_el.text_content())
                    if pm:
                        phone = pm.group(0)
                        break
            p_obj = Person(primary_org="legislature", name=name, district=district, role="Councillor")
            p_obj.add_source(COUNCIL_URL)
            if email:
                p_obj.add_contact("email", email)
            if phone:
                p_obj.add_contact("voice", phone, "legislature")
            if image:
                p_obj.image = image[0]
            yield p_obj
