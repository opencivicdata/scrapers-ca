import json
import requests

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.leg.bc.ca/members"
JSON = {
    "query": "query GetMLAsByConstituency($parliamentId: Int!) {\n  allMemberParliaments(condition: {parliamentId: $parliamentId, active: true}) {\n    nodes {\n      image: imageBySmallImageId {\n        path\n        description\n        __typename\n      }\n      constituency: constituencyByConstituencyId {\n        name\n        __typename\n      }\n      member: memberByMemberId {\n        firstName\n        lastName\n        __typename\n      }\n      isCounsel\n      isDoctor\n      isHonourable\n      party: partyByPartyId {\n        name\n        abbreviation\n        __typename\n      }\n      nodeId\n      __typename\n    }\n    __typename\n  }\n}",
    "variables": {"parliamentId": 43},
}


class BritishColumbiaPersonScraper(CanadianScraper):
    def scrape(self):
        response = requests.post(url="https://lims.leg.bc.ca/graphql", json=JSON)
        data = json.loads(response.content.decode("utf-8"))
        members = data["data"]["allMemberParliaments"]["nodes"]
        assert len(members), "No members found"
        for member in members:
            image = "https://lims.leg.bc.ca/public" + member["image"]["path"]
            district = member["constituency"]["name"]
            name = member["member"]["firstName"] + " " + member["member"]["lastName"]
            party = member["party"]["name"]

            p = Person(primary_org="legislature", name=name, district=district, role="MLA", party=party, image=image)
            p.add_source(COUNCIL_PAGE)

            yield p
