from utils import CanadianPerson as Person
from utils import CanadianScraper

CANDIDATES_PAGE = "https://www.electionsmanitoba.ca/en/Voting/Candidates/43rdGe"  # the last part of the url is for which election - change as needed


class ManitobaCandidatesPersonScraper(CanadianScraper):
    def scrape(self):
        parties = {
            "CPC-M": "Communist Party",
            "GPM": "Green Party",
            "KP": "Keystone Party",
            "MLP": "Liberal",
            "NDP": "NDP",
            "PC": "Progressive Conservative",
            "Ind.": "Independant",
        }
        division_corrections = {
            "Lagimodiere": "Lagimodière",
            "La Verendrye": "La Vérendrye",
        }
        page = self.lxmlize(CANDIDATES_PAGE)
        candidates = page.xpath('//p[@class="last-item"]')
        assert len(candidates), "No candidates found"
        for candidate in candidates:
            status = candidate.xpath('./span[@class="status"]/text()')[0]
            if status != " Official":
                continue
            name = " ".join(reversed(candidate.xpath('./span[@class="name"]/text()')[0].strip().split(","))).strip()
            if "LéAmber" in name:
                name = name.replace("é", "e")
            party = candidate.xpath('./span[@class="party"]/text()')[0]
            party = parties[party]
            division = candidate.xpath('./span[@class="division"]/text()')[0]
            if division in division_corrections:
                division = division_corrections[division]

            p = Person(primary_org="executive", name=name, role="candidate", district=division, party=party)
            p.add_source(CANDIDATES_PAGE)
            yield p
