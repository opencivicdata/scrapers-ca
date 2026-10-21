from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://iqaluit.ca/city-hall/city-council"

_ROLE_PREFIXES = ("Mayor ", "Deputy Mayor ", "Alternate Deputy Mayor ", "Councillor ")


class IqaluitPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)
        field_item = page.xpath('//div[contains(@class,"field-item")]')
        assert field_item, "field-item div not found"
        member_ps = field_item[0].xpath(".//p[./strong[normalize-space()]]")
        assert member_ps, "No member paragraphs found"

        seat = 0
        for para in member_ps:
            strong_els = para.xpath("./strong")
            if not strong_els:
                continue
            strong_text = strong_els[0].text_content().strip()

            if not any(strong_text.startswith(prefix) for prefix in _ROLE_PREFIXES):
                continue

            if strong_text.startswith("Mayor "):
                role = "Mayor"
                name = strong_text[len("Mayor ") :]
                district = "Iqaluit"
            else:
                seat += 1
                role = "Councillor"
                district = f"Iqaluit (seat {seat})"
                for prefix in ("Deputy Mayor ", "Alternate Deputy Mayor ", "Councillor "):
                    if strong_text.startswith(prefix):
                        name = strong_text[len(prefix) :]
                        break
                else:
                    name = strong_text

            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)
            yield p
