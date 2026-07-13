import re
from collections import defaultdict

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.regionofwaterloo.ca/government-and-council/council/council-members/"
CHAIR_PAGE = "https://www.regionofwaterloo.ca/government-and-council/council/council-chair/"

DISTRICTS = {
    "Doug Craig": "Cambridge",
    "Jan Liggett": "Cambridge",
    "Pam Wolf": "Cambridge",
    "Michael Harris": "Kitchener",
    "Chantal Huinink": "Kitchener",
    "Colleen James": "Kitchener",
    "Matt Rodrigues": "Kitchener",
    "Berry Vrbanovic": "Kitchener",
    "Jim Erb": "Waterloo",
    "Dorothy McCabe": "Waterloo",
    "Joe Nowak": "Waterloo",
    "Joe Gowing": "North Dumfries",
    "Natasha Salonen": "Wilmot",
    "Sandy Shantz": "Woolwich",
    "Sue Foxton": "Wellesley",
}


def _extract_district(text):
    """Try to extract the municipality from a councillor's biography text."""
    patterns = [
        # "Mayor of the City/Township of X" or "Mayor of X"
        r"Mayor of (?:the )?(?:City|Township) of (Cambridge|Kitchener|Waterloo|Wilmot|Woolwich|Wellesley|North Dumfries)",
        r"Mayor of (Cambridge|Kitchener|Waterloo|Wilmot|Woolwich|Wellesley|North Dumfries)",
        # "Regional Councillor (Kitchener)"
        r"Regional Councillor \((Cambridge|Kitchener|Waterloo|Wilmot|Woolwich|Wellesley|North Dumfries)\)",
        # "representing City/Township of X residents" or "representing X residents"
        r"representing (?:(?:City|Township) of )?(Cambridge|Kitchener|Waterloo|Wilmot|Woolwich|Wellesley|North Dumfries) residents",
        # "serve the City/Township of X on Regional Council"
        r"(?:serving|serve) (?:the )?(?:City|Township) of (Cambridge|Kitchener|Waterloo|Wilmot|Woolwich|Wellesley|North Dumfries) on Regional Council",
        # "Councillor for the City/Township of X"
        r"Councillor for (?:the )?(?:City|Township) of (Cambridge|Kitchener|Waterloo|Wilmot|Woolwich|Wellesley|North Dumfries)",
        # "elected Mayor of X" or "elected as Mayor of X"
        r"elected (?:as )?Mayor of (?:the )?(?:City|Township of )?(Cambridge|Kitchener|Waterloo|Wilmot|Woolwich|Wellesley|North Dumfries)",
        # "X residents" (broader catch-all for bio pages)
        r"\belected to Regional Council.*?(?:City|Township) of (Cambridge|Kitchener|Waterloo|Wilmot|Woolwich|Wellesley|North Dumfries)",
    ]
    for pattern in patterns:
        m = re.search(pattern, text, re.IGNORECASE)
        if m:
            return m.group(1)
    return None


class WaterlooPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        # Cards have p.heading.base-heading with "Name Role"
        # Biography links follow in the same card
        cards = page.xpath('//p[contains(@class, "heading") and contains(@class, "base-heading")]')
        assert len(cards), "No councillors found"

        seat_numbers = defaultdict(int)

        for card in cards:
            heading = card.text_content().strip()
            if heading.startswith("In Memoriam"):
                continue
            # "Karen Redman Regional Chair" or "Doug Craig Councillor"
            role_match = re.search(r"\b(Regional Chair|Councillor)\b", heading)
            if not role_match:
                continue
            role_text = role_match.group(1)
            name = heading[: heading.index(role_text)].strip()

            # Get contact info from the same container
            container = card.getparent()
            email = self.get_email(container, error=False)
            phone = self.get_phone(container, area_codes=[519, 226, 548], error=False)
            bio_link = container.xpath('.//a[contains(@href, "/council/")]/@href')
            bio_url = bio_link[0] if bio_link else None

            # Determine role and district
            if role_text == "Regional Chair":
                role = "Chair"
                district = "Waterloo"
            else:
                role = "Regional Councillor"
                district = None
                district = DISTRICTS.get(name)
                if not district and bio_url:
                    full_url = f"https://www.regionofwaterloo.ca{bio_url}" if bio_url.startswith("/") else bio_url
                    bio_page = self.lxmlize(full_url)
                    bio_text = bio_page.text_content()
                    district = _extract_district(bio_text)

                if district in ("Cambridge", "Kitchener", "Waterloo"):
                    seat_numbers[district] += 1
                    district = f"{district} (seat {seat_numbers[district]})"
                elif not district:
                    raise Exception(f"No district for {name}")

            p = Person(primary_org="legislature", name=name, district=district, role=role)
            if bio_url:
                full_url = f"https://www.regionofwaterloo.ca{bio_url}" if bio_url.startswith("/") else bio_url
                bio_page = self.lxmlize(full_url)
                image = bio_page.xpath('.//div[contains(@class, "img-right")]//img/@src')
                if image:
                    p.image = image[0]
                p.add_source(full_url)

            if email:
                p.add_contact("email", email)
            if phone:
                p.add_contact("voice", phone, "legislature")
            p.add_source(COUNCIL_PAGE)
            yield p
