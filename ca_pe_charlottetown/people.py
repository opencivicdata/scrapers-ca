import re

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.charlottetown.ca/mayor___council/city_council/meet_my_councillor"


class CharlottetownPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE, user_agent="Mozilla/5.0")

        nodes = page.xpath('//div[@id="ctl00_ContentPlaceHolder1_ctl13_divContent"]/*')
        groups = [[]]
        for node in nodes:
            if node.tag == "hr":
                groups.append([])
            else:
                groups[-1].append(node)

        assert len(groups), "No councillors found"
        for group in groups:
            para = group[0]
            text = para.xpath(".//strong[1]/text()")[0]
            if "Deputy Mayor" in text:
                role = "Councillor"
                match = re.search(r"Deputy Mayor (.+) - (Ward \d+)", text)
                district = match.group(2)
            elif "Mayor" in text:
                role = "Mayor"
                match = re.search(r"Mayor (.+)", text)
                district = "Charlottetown"
            else:
                role = "Councillor"
                match = re.search(r"Councillor (.+) - (Ward \d+)", text)
                district = match.group(2)

            image = para.xpath(".//@src")[0]
            name = match.group(1).split("(")[0]

            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)

            p.image = image

            email = self.get_email(para)
            p.add_contact("email", email)

            for text in para.xpath('.//strong[contains(., "Phone")]/following-sibling::text()'):
                if re.search(r"\d", text):
                    match = re.search(r"(.+) \((.+)\)", text)
                    contact_type = "fax" if match.group(2) == "Fax" else "voice"
                    p.add_contact(contact_type, match.group(1), match.group(2))

            yield p
