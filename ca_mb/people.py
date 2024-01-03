from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "http://www.gov.mb.ca/legislature/members/mla_list_alphabetical.html"


def get_party(abbreviation):
    return {
        "MAN": "Manitoba Party",
        "NDP": "New Democratic Party of Manitoba",
        "PC": "Progressive Conservative Party of Manitoba",
        "L": "Manitoba Liberal Party",
        "LIB": "Manitoba Liberal Party",
        "IND": "Independent",
        "IND LIB": "Independent Liberal",
    }[abbreviation]


class ManitobaPersonScraper(CanadianScraper):
    def scrape(self):
        member_page = self.lxmlize(COUNCIL_PAGE, encoding="utf-8")
        table = member_page.xpath("//table")[0]
        rows = table.xpath(".//tr")[1:]
        assert len(rows), "No members found"
        for row in rows:
            (namecell, constitcell, partycell) = row.xpath(".//td")
            full_name = namecell.text_content().strip()
            if full_name.lower() == "vacant":
                continue
            (last, first) = full_name.split(",")
            name = first.replace("Hon.", "").strip() + " " + last.title().strip()
            district = " ".join(constitcell.text_content().split())
            if district == "Portage-la-Prairie":
                district = district.replace("-", " ")
            party = get_party(partycell.text)

            url = namecell.xpath(".//a")[0].get("href")

            page = self.lxmlize(url)
            email = self.get_email(page)

            p = Person(primary_org="legislature", name=name, district=district, role="MLA", party=party)
            p.add_source(COUNCIL_PAGE)
            p.add_source(url)
            p.add_contact("email", email)

            image = page.xpath('//img[@class="page_graphic"]/@src')
            if image:
                p.image = image[0]

            yield p
