import re

from opencivicdata.divisions import Division
from pupa.scrape import Organization

from utils import CanadianPerson as Person
from utils import CanadianScraper

LIST_PAGE = "https://www.civicinfo.bc.ca/people"


class BritishColumbiaMunicipalitiesPersonScraper(CanadianScraper):
    birth_date = 1900

    def scrape(self):
        exclude_districts = {
            # Existing scrapers
            "Abbotsford",
            "Burnaby",
            "Coquitlam",
            "Kelowna",
            "Langley",
            "New Westminster",
            "Richmond",
            "Saanich",
            "Surrey",
            "Vancouver",
            "Victoria",
        }
        excluded_district_types = {
            "Regional District",
            "Indian Government District",
            "Islands Trust",
            "Mountain Resort Municipality",
        }
        division_corrections = {
            "100 Mile House": "One Hundred Mile House",
        }

        processed_ids = set()
        exclude_divisions = {}
        processed_divisions = set()
        infixes = {
            "CY": "City",
            "DM": "District",
            "IGD": "District",
            "IM": "Municipal",
            "RGM": "Regional",
            "T": "Town",
            "VL": "Village",
            "RDA": "District",
        }
        organizations = {}
        # Create list mapping names to IDs.
        names_to_ids = {}
        for division in Division.get("ocd-division/country:ca").children("csd"):
            type_id = division.id.rsplit(":", 1)[1]
            if type_id.startswith("59"):
                if division.attrs["classification"] == "IRI":
                    continue
                if division.name in names_to_ids:
                    names_to_ids[division.name] = None
                else:
                    names_to_ids[division.name] = division.id

        # Scrape list of municpalities.
        list_page = self.lxmlize(LIST_PAGE)
        municipalities = list_page.xpath('//select[@name="lgid"]/option')
        assert len(municipalities), "No municipalities found"

        # Iterate through each municipality.
        for municipality in municipalities:
            municipality_text = municipality.text
            municipal_type = municipality_text[municipality_text.find("(") + 1 : municipality_text.find(")")]
            if municipal_type in excluded_district_types:
                continue

            municipal_id = municipality.get("value")
            division_name = municipality_text.split(" (")[0]
            division_name = division_corrections.get(division_name, division_name)

            record_url = LIST_PAGE + "?stext=&type=ss&lgid=" + municipal_id + "&agencyid=+"

            # If we have a municipal ID, process that municipality.
            if municipal_id and municipal_id.strip():
                # Get division ID from municipal name and filter out duplicates or unknowns.
                if division_name in exclude_districts or division_name in processed_divisions:
                    continue
                division_id = names_to_ids[division_name]
                if not isinstance(division_id, str):
                    continue
                if division_id in exclude_divisions:
                    continue
                if division_id in processed_ids:
                    raise Exception(f"unhandled collision: {division_id}")
                division = Division.get(division_id)
                processed_divisions.add(division_name)

                # Get division name and create org.
                division_name = division.name
                organization_name = "{} {} Council".format(division_name, infixes[division.attrs["classification"]])
                if division_id not in processed_ids:
                    processed_ids.add(division_id)
                    organizations[division_id] = Organization(name=organization_name, classification="government")
                    organizations[division_id].add_source(record_url)
                organization = organizations[division_id]
                organization.add_post(role="Mayor", label=division_name, division_id=division_id)
                organization.add_post(role="Councillor", label=division_name, division_id=division_id)

                # Load records for municipality.
                municipal_page = self.lxmlize(record_url)
                number_of_records_text = municipal_page.xpath("//main/h4/text()")
                number_of_records = int(re.search(r"\d+", number_of_records_text[0]).group())

                # Collate mayor and councillor representatives on first page of records.
                leader_reps = municipal_page.xpath('//main/ol/li[contains(., "Mayor")][not(contains(., "Chief"))]')
                councillor_reps = municipal_page.xpath('//main/ol/li[contains(., "Councillor")]')

                # Iterate through additional pages of records if they exists adding reps.
                if number_of_records > 10:
                    quotient, remainder = divmod(number_of_records, 10)
                    number_of_pages = quotient + int(bool(remainder))
                    for i in range(2, number_of_pages + 1):
                        municipal_page = self.lxmlize(record_url + "&pn=" + str(i))
                        additional_leader_reps = municipal_page.xpath(
                            '//main/ol/li[contains(., "Mayor")][not(contains(., "Chief"))][not(contains(., "Assistant"))]'
                        )
                        leader_reps.extend(additional_leader_reps)
                        additional_councillor_reps = municipal_page.xpath('//main/ol/li[contains(., "Councillor")]')
                        councillor_reps.extend(additional_councillor_reps)

                # Create person records for all mayor and councillor representatives.
                for leader_rep in leader_reps:
                    yield self.person_data(leader_rep, division_id, division_name, "Mayor", organization_name)
                for councillor_rep in councillor_reps:
                    yield self.person_data(councillor_rep, division_id, division_name, "Councillor", organization_name)

        # Iterate through each organization.
        for organization in organizations.values():
            yield organization

    def person_data(self, representative, division_id, division_name, role, organization_name):
        # Corrections and tweaks.
        duplicate_names = {
            "Colleen Evans",
            "Kim Watt-Senner",
        }
        name_corrections = {
            "Claire l Moglove": "Claire Moglove",
            "KSenya Dorwart": "Ksenya Dorwart",
        }
        email_corrections = {"sharrison@qualicumbeach,com": "sharrison@qualicumbeach.com"}

        # Get name.
        representative_name = re.sub(" +", " ", str(representative.xpath("a/b/text()")[0]).strip())
        representative_name = name_corrections.get(representative_name, representative_name)

        # Get phone.
        representative_phone = str(representative.xpath('text()[contains(., "Phone")]'))[12:-2].replace("-", "")

        # Get email.
        email_scrape = representative.xpath('a[contains(@href,"mailto:")]/text()')
        if email_scrape:
            representative_email = email_scrape[0]
            representative_email = email_corrections.get(representative_email, representative_email)

        # Create record and append contact data.
        p = Person(
            primary_org="government",
            primary_org_name=organization_name,
            name=representative_name,
            district=division_name,
            role=role,
        )
        p.add_source(LIST_PAGE)

        # Handle duplicate names.
        if representative_name in duplicate_names:
            p.birth_date = str(self.birth_date)
            self.birth_date += 1
        if email_scrape:
            p.add_contact("email", representative_email)
        if representative_phone and len(representative_phone) == 10:
            p.add_contact("voice", representative_phone, "legislature")

        p._related[0].extras["boundary_url"] = "/boundaries/census-subdivisions/{}/".format(
            division_id.rsplit(":", 1)[1]
        )

        return p
