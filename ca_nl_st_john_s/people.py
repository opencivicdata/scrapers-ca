from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.stjohns.ca/your-government/mayor-and-council/"


class StJohnsPersonScraper(CanadianScraper):
    def scrape(self):
        councillor_seat_number = 1

        page = self.lxmlize(COUNCIL_PAGE)
        councillors = page.xpath('//a[contains(@href, "/your-government/mayor-and-council/") and .//img]/@href')
        assert len(councillors), "No councillors found"
        for url in councillors:
            if not url.startswith("http"):
                url = "https://www.stjohns.ca" + url
            profile_page = self.lxmlize(url)
            h1_elements = profile_page.xpath("//main//h1") or profile_page.xpath("//h1")
            h1_text = h1_elements[0].text_content().strip()
            # h1 is "Mayor Name", "Deputy Mayor Name", or "Councillor Name"
            if h1_text.startswith("Deputy Mayor "):
                role = "Deputy Mayor"
                name = h1_text[len("Deputy Mayor ") :]
            elif h1_text.startswith("Mayor "):
                role = "Mayor"
                name = h1_text[len("Mayor ") :]
            elif h1_text.startswith("Councillor "):
                role = "Councillor"
                name = h1_text[len("Councillor ") :]
            else:
                continue

            # Find district from first paragraph text
            paragraphs = profile_page.xpath("//main//p")
            description = paragraphs[0].text_content() if paragraphs else ""
            if "Ward" in description:
                index = description.find("Ward")
                district = description[index : index + 6]
            else:
                district = "St. John's"
                if role not in ("Mayor", "Deputy Mayor"):
                    role = "Councillor at Large"
                    district = f"St. John's (seat {councillor_seat_number})"
                    councillor_seat_number += 1

            email = self.get_email(profile_page, error=False)
            phone = self.get_phone(profile_page, error=False)
            photo_nodes = profile_page.xpath('//img[contains(@src, "/media/")]/@src')
            photo = photo_nodes[0] if photo_nodes else None
            if photo and not photo.startswith("http"):
                photo = "https://www.stjohns.ca" + photo

            p = Person(primary_org="legislature", name=name, district=district, role=role)
            if photo:
                p.image = photo
            if phone:
                p.add_contact("voice", phone, "legislature")
            if email:
                p.add_contact("email", email)
            p.add_source(COUNCIL_PAGE)
            p.add_source(url)

            yield p
