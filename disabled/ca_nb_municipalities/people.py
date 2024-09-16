import re

from opencivicdata.divisions import Division
from pupa.scrape import Organization

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "http://www2.gnb.ca/content/gnb/en/departments/elg/local_government/content/community_profiles.html"


class NewBrunswickMunicipalitiesPersonScraper(CanadianScraper):
    def scrape(self):
        exclude_divisions = {
            "ocd-division/country:ca/csd:1301006",  # Saint John
            "ocd-division/country:ca/csd:1307022",  # Moncton
            "ocd-division/country:ca/csd:1310032",  # Fredericton
        }
        expected_roles = {
            "Mayor",
            "Councillor",
        }
        unique_roles = {
            "Mayor",
        }
        classifications = {
            "Cities": "City",
            "Towns": "Town",
            "Villages": "Village",
            "Rural Communities": "Community",
            "Regional Municipality": "Regional",
        }
        corrections = {
            "Beaubassin-est/East": "Beaubassin East",
            "Lac-Baker": "Lac Baker",
            "Saint-François-de-Madawaska": "Saint-François de Madawaska",
            "Saint-Hilaire": "Saint Hilaire",
        }
        unknown_names = {
            "Haut-Madawaska",  # incorporated after Census 2016
        }
        duplicate_names = {
            "Denis Savoie",
            "Josée Levesque",
            "Luc Levesque",
        }

        names_to_ids = {}
        for division in Division.get("ocd-division/country:ca").children("csd"):
            type_id = division.id.rsplit(":", 1)[1]
            if type_id.startswith("13"):
                if division.attrs["classification"] == "P":
                    continue
                if division.name in names_to_ids:
                    raise Exception(f"unhandled collision: {division.name}")
                else:
                    names_to_ids[division.name] = division.id

        page = self.lxmlize(COUNCIL_PAGE)
        list_links = page.xpath('//div[@id="sidebar"]//div[contains(@class, "list")][1]//a')

        birth_date = 1900
        seen = set()

        assert len(list_links), "No list items found"
        for list_link in list_links:
            page = self.lxmlize(list_link.attrib["href"])
            detail_urls = page.xpath("//td[1]//@href")

            assert len(detail_urls), "No municipalities found"
            for detail_url in detail_urls:
                page = self.lxmlize(detail_url, encoding="utf-8")
                division_name = re.sub(r"\ASt\b\.?", "Saint", page.xpath("//h1/text()")[0].split(" - ", 1)[1])
                division_name = corrections.get(division_name, division_name)

                if division_name in unknown_names:
                    continue
                division_id = names_to_ids[division_name]
                if division_id in exclude_divisions:
                    continue
                if division_id in seen:
                    raise Exception(f"unhandled collision: {division_id}")

                seen.add(division_id)
                division_name = Division.get(division_id).name
                organization_name = f"{division_name} {classifications[list_link.text]} Council"
                organization = Organization(name=organization_name, classification="government")
                organization.add_source(detail_url)

                address = ", ".join(page.xpath('//div[@class="left_contents"]/p[1]/text()'))

                contacts = page.xpath('//div[@class="left_contents"]/p[contains(., "Contact")]/text()')
                phone = contacts[0].split(":")[1]
                if len(contacts) > 1:
                    fax = contacts[1].split(":")[1]
                email = self.get_email(page, '//div[@class="left_contents"]', error=False)

                url = page.xpath('//div[@class="left_contents"]//@href[not(contains(., "mailto:"))]')
                if url:
                    url = url[0]

                groups = page.xpath('//div[contains(@class, "right_contents")]/p')
                assert len(groups), "No groups found"
                for p in groups:
                    role = p.xpath("./b/text()")[0].rstrip("s")
                    if role not in expected_roles:
                        raise Exception(f"unexpected role: {role}")

                    councillors = p.xpath("./text()")
                    assert len(councillors), "No councillors found"
                    for seat_number, name in enumerate(councillors, 1):
                        if "vacant" in name.lower():
                            continue

                        district = division_name if role in unique_roles else f"{division_name} (seat {seat_number})"

                        organization.add_post(role=role, label=district, division_id=division_id)

                        p = Person(
                            primary_org="government",
                            primary_org_name=organization_name,
                            name=name,
                            district=district,
                            role=role,
                        )
                        p.add_source(COUNCIL_PAGE)
                        p.add_source(list_link.attrib["href"])
                        p.add_source(detail_url)

                        if name in duplicate_names:
                            p.birth_date = str(birth_date)
                            birth_date += 1

                        p.add_contact("address", address, "legislature")
                        # @see https://en.wikipedia.org/wiki/Area_code_506
                        if phone:
                            p.add_contact("voice", phone, "legislature", area_code=506)
                        if fax:
                            p.add_contact("fax", fax, "legislature", area_code=506)
                        if email:
                            p.add_contact("email", email)
                        if url:
                            p.add_link(url)

                        p._related[0].extras["boundary_url"] = "/boundaries/census-subdivisions/{}/".format(
                            division_id.rsplit(":", 1)[1]
                        )

                        yield p

                yield organization
