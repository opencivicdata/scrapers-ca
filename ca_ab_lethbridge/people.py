from utils import CanadianPerson as Person
from utils import CanadianScraper

BASE_URL = "https://www.lethbridge.ca"
COUNCIL_PAGE = f"{BASE_URL}/council-administration-governance/mayor-and-councillors/councillors-office"
MAYOR_PAGE = f"{BASE_URL}/council-administration-governance/mayor-and-councillors/mayors-office"


class LethbridgePersonScraper(CanadianScraper):
    def scrape_mayor(self):
        page = self.lxmlize(MAYOR_PAGE)

        # Use the first p following the biography h4 (e.g. "Mayor Hyggen"), which starts "FirstName LastName was..."
        bio_paragraphs = page.xpath("//h4[contains(., 'Mayor') and not(contains(., 'Watch'))]/following-sibling::p")
        bio_text = bio_paragraphs[0].text_content().strip()
        # Extract "FirstName LastName" from "FirstName LastName was ..." or fallback to first two words
        name_match = bio_text.split(" was ")[0].strip() if " was " in bio_text else " ".join(bio_text.split()[:2])
        name = name_match

        p = Person(primary_org="legislature", name=name, district="Lethbridge", role="Mayor")
        p.image = page.xpath("//img/@src")[0]
        p.add_source(MAYOR_PAGE)

        return p

    def scrape_person(self, url, seat_number):
        page = self.lxmlize(url)
        name = page.xpath('//h1[contains(@class, "heading main base-heading")]')[0].text_content().split(",")[0]

        p = Person(
            primary_org="legislature",
            name=name,
            district=f"Lethbridge (seat {seat_number + 1})",
            role="Councillor",
        )

        imgs = page.xpath('//img[contains(@src, "/media/") and not(contains(@src, "logo"))]/@src')
        if imgs:
            p.image = imgs[0] if imgs[0].startswith("http") else BASE_URL + imgs[0]
        p.add_source(COUNCIL_PAGE)
        p.add_source(url)

        return p

    def scrape(self):
        yield self.scrape_mayor()

        page = self.lxmlize(COUNCIL_PAGE)
        seen = set()
        councillor_urls = []
        for a in page.xpath('//a[contains(@href, "-councillor/")]'):
            href = a.get("href")
            if href not in seen and href != COUNCIL_PAGE.replace(BASE_URL, ""):
                seen.add(href)
                councillor_urls.append(href if href.startswith("http") else BASE_URL + href)
        assert councillor_urls, "No councillors found"
        for seat_number, url in enumerate(councillor_urls):
            yield self.scrape_person(url, seat_number)
