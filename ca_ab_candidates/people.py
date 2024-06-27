from utils import CanadianPerson as Person
from utils import CanadianScraper

CANDIDATES_PAGE = "https://efpublic.elections.ab.ca/efCandidatesPGE.cfm?MODE=BROWSE&MID=FC_2023&OFSFID=101&EDS=ALL"


class AlbertaCandidatesPersonScraper(CanadianScraper):
    def scrape(self):
        party_corrections = {
            "United Conservative Party of Alberta": "United Conservative Party",
            "Advantage Party of Alberta": "Alberta Advantage Party",
            "The Independence Party of Alberta": "Alberta Independance Party",
        }
        district_corrections = {
            "Edmonton-Mcclung": "Edmonton-McClung",
            "Calgary-Bhullar-Mccall": "Calgary-McCall",
            "Fort Mcmurray-Wood Buffalo": "Fort McMurray-Wood Buffalo",
            "Fort Mcmurray-Lac La Biche": "Fort McMurray-Lac La Biche",
        }
        page = self.lxmlize(CANDIDATES_PAGE)
        candidates = page.xpath('//tr[contains(./td/@class, "ListCellW")]')
        assert len(candidates), "No candidates found"
        for candidate in candidates:
            name = candidate.xpath("./td[1]/text()")[0].title()
            if "(" in name:
                continue
            district = candidate.xpath("./td[2]/text()")[0].split(" ", 1)[1].title().strip()
            if district in district_corrections:
                district = district_corrections[district]
            party = candidate.xpath("./td[2]/text()")[1].strip()
            if party in party_corrections:
                party = party_corrections[party]
            p = Person(primary_org="executive", name=name, district=district, role="candidate", party=party)
            p.add_source(CANDIDATES_PAGE)
            yield p
