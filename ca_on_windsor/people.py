import json
import re

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.citywindsor.ca/mayor-and-council/city-councillors"
DATA_URL = "https://www.citywindsor.ca/v1/Search/portal?searchText="
BASE_URL = "https://www.citywindsor.ca"


class WindsorPersonScraper(CanadianScraper):
    def scrape(self):
        # The page loads all of the data with javascript
        # This post request is what it uses to get the council members listing
        data_request = {
            "searchOptions": {
                "includeTotalCount": True,
                "filter": "EUMSearchSource eq 'user' and search.ismatch('8a56d84b-ba8b-4ca4-a16d-67d1734a00a2','MemberGroups')",
                "size": 25,
                "skip": 0,
            },
            "highlightFields": ["PageContent"],
            "EUMSearchSources": ["user"],
            "Select": [
                "id",
                "Slug",
                "mail",
                "displayName",
                "surname",
                "givenName",
                "companyName",
                "Twitter",
                "HasImage",
                "jobTitle",
                "LinkedIn",
                "Blog",
                "department",
            ],
            "OrderBy": ["department asc"],
        }
        data = json.loads(self.post(DATA_URL, json=data_request).text)
        assert data["totalCount"] > 0, "No councillors found"
        for response_item in data["value"]:
            item = response_item["document"]
            url = f"{BASE_URL}/directory/{item['Slug']}"
            page = self.lxmlize(url)
            phone = self.get_phone(page)
            email = item["mail"]
            name = item["displayName"]
            # Leading 0 before ward numbers
            district = re.sub(" 0+", " ", item["department"])
            # Councillors listed as City Councillor
            role = item["jobTitle"].replace("City ", "")
            if district == "Mayor":
                district = "Windsor"
            p = Person(primary_org="legislature", name=name, district=district, role=role)
            if item["HasImage"]:
                image = f"{BASE_URL}/profileimages/250/{item['id']}.jpg"
                p.image = image
            p.add_contact("email", email)
            if phone:
                p.add_contact("voice", phone, "legislature")
            p.add_source(COUNCIL_PAGE)
            p.add_source(url)

            yield p
