import json
from textwrap import dedent

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.leg.bc.ca/members"


class BritishColumbiaPersonScraper(CanadianScraper):
    def scrape(self):
        response = self.post(
            url="https://lims.leg.bc.ca/graphql",
            json={
                "query": dedent("""\
                query GetMLAsByConstituency($parliamentId: Int!) {
                  allMemberParliaments(condition: {parliamentId: $parliamentId, active: true}) {
                    nodes {
                      image: imageBySmallImageId {
                        path
                        description
                        __typename
                      }
                      constituency: constituencyByConstituencyId {
                        name
                        __typename
                      }
                      member: memberByMemberId {
                        firstName
                        lastName
                        __typename
                      }
                      isCounsel
                      isDoctor
                      isHonourable
                      party: partyByPartyId {
                        name
                        abbreviation
                        __typename
                      }
                      nodeId
                      __typename
                    }
                    __typename
                  }
                }"""),
                "variables": {"parliamentId": 43},
            },
        )
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
