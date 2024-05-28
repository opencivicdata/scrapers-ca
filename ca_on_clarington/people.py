import re

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "http://www.clarington.net/index.php?content=townhall/council"


class ClaringtonPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        councillors = page.xpath("//h2")
        assert len(councillors), "No councillors found"
        for person_header_elem in councillors:
            role, name_post = person_header_elem.text.split(" - ")
            try:
                name, caps_post = re.match(r"(.+) \((.+)\)", name_post).groups()
                post = caps_post.title()
            except AttributeError:
                name = name_post
                post = "Clarington"
            email = person_header_elem.xpath("./following-sibling::a[1]/@href")[0][len("mailto:") :]
            photo_url = person_header_elem.xpath("./following-sibling::img[1]/@src")[0]
            p = Person(primary_org="legislature", name=name, district=post, role=role, image=photo_url)
            p.add_source(COUNCIL_PAGE)
            p.add_contact("email", email)
            yield p
