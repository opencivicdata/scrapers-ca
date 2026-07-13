import re
from urllib.parse import quote

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.dnv.org/government-administration/mayor-and-councillors"
API_PAGE = "https://simplicity-api.dnv.org/public/webpage/path/" + quote(
    "/government-administration/mayor-and-councillors", safe=""
)


class NorthVancouverPersonScraper(CanadianScraper):
    def flatten_text(self, node):
        parts = []
        if isinstance(node, dict):
            if node.get("type") == "text":
                parts.append(node.get("text", ""))
            for child in node.get("content", []):
                parts.extend(self.flatten_text(child))
        elif isinstance(node, list):
            for child in node:
                parts.extend(self.flatten_text(child))
        return parts

    def scrape(self):
        webpage = self.get(API_PAGE).json()
        model = self.get(f"https://simplicity-api.dnv.org/public/model/{webpage['model']}").json()

        tables = [
            node
            for field in model["fields"]
            for value in field.get("values", [])
            for component in value.get("value", [])
            for node in component.get("richtext", {}).get("content", [])
            if node.get("type") == "table"
        ]
        assert len(tables), "No council member table found"

        rows = tables[0].get("content", [])[1:]
        assert len(rows) == 7, "Expected 7 council members"

        councillor_seat_number = 1
        for row in rows:
            cells = row.get("content", [])
            title = " ".join(self.flatten_text(cells[0])).strip()
            phone = " ".join(self.flatten_text(cells[1])).strip()
            email = " ".join(self.flatten_text(cells[2])).strip()

            if title.startswith("Mayor "):
                role = "Mayor"
                name = title.replace("Mayor ", "", 1)
                district = "North Vancouver"
            else:
                role = "Councillor"
                name = title
                district = f"North Vancouver (seat {councillor_seat_number})"
                councillor_seat_number += 1

            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)
            p.add_source(API_PAGE)

            if email:
                p.add_contact("email", email)

            phone_match = re.search(r"(?:604|778)[-. ]\d{3}[-. ]\d{4}", phone)
            if phone_match:
                p.add_contact("voice", phone_match.group(0), "legislature")

            yield p
