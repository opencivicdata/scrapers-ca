import re
from collections import defaultdict

from pupa.scrape import Organization, Post

from utils import CanadianPerson as Person
from utils import CSVScraper


class CanadaMunicipalitiesPersonScraper(CSVScraper):
    csv_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRrGXQy8qk16OhuTjlccoGB4jL5e8X1CEqRbg896ufLdh67DQk9nuGm-oufIT0HRMPEnwePw2HDx1Vj/pub?gid=0&single=true&output=csv"
    encoding = "utf-8"

    """
    Returns whether the row should be imported.
    """

    def is_valid_row(self, row):
        return super().is_valid_row(row) and row["organization"]

    def scrape(self):
        organizations = {}
        seat_numbers = defaultdict(lambda: defaultdict(int))

        reader = self.csv_reader(
            self.csv_url, delimiter=self.delimiter, header=True, encoding=self.encoding, skip_rows=self.skip_rows
        )
        reader.fieldnames = [self.header_converter(field) for field in reader.fieldnames]
        for row in reader:
            try:
                if self.is_valid_row(row):
                    for key, corrections in self.corrections.items():
                        if not isinstance(corrections, dict):
                            row[key] = corrections(row[key])
                        elif row[key] in corrections:
                            row[key] = corrections[row[key]]

                    organization_classification = "legislature"

                    organization_name = row["organization"]
                    organization_key = organization_name.lower()
                    if organization_key in organizations:
                        organization = organizations[organization_key]
                    else:
                        organization = Organization(organization_name, classification=organization_classification)
                        organization.add_source(self.csv_url)
                        yield organization
                        organizations[organization_key] = organization

                    if not row["primary role"]:
                        row["primary role"] = "Councillor"

                    role = row["primary role"]

                    post = Post(role=role, label=organization_name, organization_id=organization._id)
                    yield post

                    name = row["name"].strip(" .,")

                    district = row["district name"]

                    if self.many_posts_per_area and role not in self.unique_roles:
                        seat_numbers[role][district] += 1
                        district = f"{district} (seat {seat_numbers[role][district]})"

                    p = Person(
                        primary_org=organization_classification,
                        name=name,
                        district=district,
                        role=role,
                        party=row.get("party name"),
                    )
                    p.add_source(self.csv_url)

                    if row.get("gender"):
                        p.gender = row["gender"]
                    if row.get("photo url"):
                        p.image = row["photo url"]

                    if row.get("source url"):
                        p.add_source(row["source url"].strip(" .,"))

                    if row.get("website"):
                        p.add_link(row["website"], note="web site")
                    if row.get("facebook"):
                        p.add_link(re.sub(r"[#?].+", "", row["facebook"]))
                    if row.get("twitter"):
                        p.add_link(row["twitter"])

                    if row["email"]:
                        p.add_contact("email", row["email"].strip(" .,"))
                    if row["address"]:
                        p.add_contact("address", row["address"], "legislature")
                    if row.get("phone"):
                        p.add_contact("voice", row["phone"], "legislature")
                    if row.get("fax"):
                        p.add_contact("fax", row["fax"], "legislature")
                    if row.get("cell"):
                        p.add_contact("cell", row["cell"], "legislature")
                    if row.get("birth date"):
                        p.birth_date = row["birth date"]

                    if row.get("incumbent"):
                        p.extras["incumbent"] = row["incumbent"]

                    if name in self.other_names:
                        for other_name in self.other_names[name]:
                            p.add_name(other_name)

                    # Validate person entity so that we can catch the exception if needed.
                    p.validate()

                    yield p
            except Exception:
                pass
