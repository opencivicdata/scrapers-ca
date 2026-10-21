from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.centrewellington.ca/township-services/mayor-and-council/"


class CentreWellingtonPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)
        mayor = page.xpath('//h3[starts-with(normalize-space(), "Mayor ")]')
        councillors = page.xpath('//a[starts-with(normalize-space(), "Councillor ")]')
        assert len(mayor) == 1, "Expected 1 mayor"
        assert len(councillors) >= 6, "Expected at least 6 councillor links"

        p = Person(
            primary_org="legislature",
            name=mayor[0].text_content().strip()[len("Mayor ") :],
            district="Centre Wellington",
            role="Mayor",
        )
        p.add_source(COUNCIL_PAGE)
        yield p

        seen = set()
        ward_number = 1
        for link in councillors:
            title = link.text_content().strip()
            if title in seen:
                continue
            seen.add(title)
            p = Person(
                primary_org="legislature",
                name=title[len("Councillor ") :],
                district=f"Ward {ward_number}",
                role="Councillor",
            )
            p.add_source(COUNCIL_PAGE)
            p.add_source(link.get("href"))
            yield p
            ward_number += 1
            if ward_number > 6:
                break
