import os
import re
import subprocess
import tempfile

from pupa.scrape import Organization

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "http://www.community.gov.yk.ca/pdf/loc_govdir.pdf"


class YukonMunicipalitiesPersonScraper(CanadianScraper):
    def scrape(self):
        response = self.get(COUNCIL_PAGE).content
        with tempfile.NamedTemporaryFile(delete_on_close=False) as pdf:
            pdf.write(response)

        data = subprocess.check_output(["pdftotext", "-layout", pdf.name, "-"])  # noqa: S603,S607
        data = re.split(r"\n\s*\n", data)
        for municipality in data:
            if "Councillors" not in municipality:
                continue
            lines = municipality.split("\n")
            if "Page" in lines[0]:
                lines.pop(0)
                if not lines[0].strip():
                    lines.pop(0)
            col1end = re.search(r"\s{2,}(\w)", lines[0].strip()).end()
            col2end = re.search(r":\s{2,}(\w)", lines[0].strip()).end()

            if "Council" in lines[1]:
                address = lines[2][: col1end - 1].strip() + " " + lines[3][: col1end - 1].strip()
                district = lines[0][: col1end - 1].strip() + " " + lines[1][: col1end - 1].strip()
            else:
                address = lines[1][: col1end - 1].strip() + " " + lines[2][: col1end - 1].strip()
                district = lines[0][: col1end - 1].strip()

            organization = Organization(
                name=district + " Council",
                classification="legislature",
                jurisdiction_id=self.jurisdiction.jurisdiction_id,
            )
            organization.add_source(COUNCIL_PAGE)
            yield organization

            phone = re.findall(r"(?<=Phone: )\(?(\d{3}[\)-] ?\d{3}-\d{4})", municipality)[0].replace(") ", "-")
            email = re.findall(r"(?<=E-mail:) (\S*)", municipality)[0]
            fax = None
            if "Fax" in municipality:
                fax = re.findall(r"(?<=Fax: )\(?(\d{3}[\)-] ?\d{3}-\d{4})", municipality)[0].replace(") ", "-")
            website = None
            if "Website" in municipality:
                website = re.findall(r"((http:\/\/|www.)(\S*))", municipality)[0][0]

            councillor_or_mayor = False
            for line in lines:
                if "Mayor:" in line:
                    councillor_or_mayor = True
                    role = "Mayor"
                    continue
                if "Councillors" in line:
                    councillor_or_mayor = True
                    role = "Councillor"
                    continue
                if councillor_or_mayor:
                    councillor = line[col1end - 1 : col2end - 1].strip()
                    if not councillor:
                        continue
                    p = Person(primary_org="legislature", name=councillor, district=district)
                    p.add_source(COUNCIL_PAGE)
                    membership = p.add_membership(organization, role=role, district=district)
                    membership.add_contact_detail("address", address, "legislature")
                    membership.add_contact_detail("voice", phone, "legislature")
                    membership.add_contact_detail("email", email)
                    if fax:
                        membership.add_contact_detail("fax", fax, "legislature")
                    if website:
                        p.add_link(website)
                    yield p

        os.unlink(pdf.name)
