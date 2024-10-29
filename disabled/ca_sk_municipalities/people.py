import os
import re
import subprocess
import tempfile

from pupa.scrape import Organization

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "http://www.municipal.gov.sk.ca/Programs-Services/Municipal-Directory-pdf"
# See also HTML format http://www.mds.gov.sk.ca/apps/Pub/MDS/welcome.aspx


class SaskatchewanMunicipalitiesPersonScraper(CanadianScraper):
    def scrape(self):
        response = self.get(COUNCIL_PAGE).read()
        with tempfile.NamedTemporaryFile(delete_on_close=False) as pdf:
            pdf.write(response)

        data = subprocess.check_output(["pdftotext", "-layout", pdf.name, "-"])  # noqa: S603,S607

        data = data.splitlines(keepends=True)
        pages = []
        page = []
        for line in data:
            if line.strip() and "Page" not in line and "CITIES" not in line and "NORTHERN TOWNS, VILLAGES" not in line:
                page.append(line)
            elif page:
                pages.append(page)
                page = []

        districts = []
        for page in pages:
            index = re.search(r"(\s{6,})", page[0])
            index = index.end() - 1 if index else -1
            dist1 = []
            dist2 = []
            for line in page:
                dist1.append(line[:index].strip())
                dist2.append(line[index:].strip())
            districts.append(dist1)
            districts.append(dist2)

        for district in districts:
            district_name = district.pop(0).split(",")[0].title()

            org = Organization(
                name=district_name + " Council",
                classification="legislature",
                jurisdiction_id=self.jurisdiction.jurisdiction_id,
            )
            org.add_source(COUNCIL_PAGE)

            councillors = []
            contacts = {}
            for i, line in enumerate(district):
                if "Phone" in line:
                    phone = line.split(":")[1].replace("(", "").replace(") ", "-").strip()
                    if phone:
                        contacts["voice"] = phone
                if "Fax" in line:
                    fax = line.split(":")[1].replace("(", "").replace(") ", "-").strip()
                    if fax:
                        contacts["fax"] = fax
                if "E-Mail" in line:
                    email = line.split(":")[1].strip()
                    if email:
                        contacts["email"] = email
                if "Address" in line and line.split(":")[1].strip():
                    address = line.split(":")[1].strip() + ", " + ", ".join(district[i + 1 :]).replace(" ,", "")
                    contacts["address"] = address
                if "Mayor" in line or "Councillor" in line or "Alderman" in line:
                    councillor = (
                        line.split(":")[1]
                        .replace("Mr.", "")
                        .replace("Mrs.", "")
                        .replace("Ms.", "")
                        .replace("His Worship", "")
                        .replace("Her Worship", "")
                        .strip()
                    )
                    role = line.split(":")[0].strip()
                    if councillor:
                        councillors.append([councillor, role])

            if not councillors:
                continue
            yield org
            for councillor in councillors:
                p = Person(primary_org="legislature", name=councillor[0], district=district_name)
                p.add_source(COUNCIL_PAGE)
                membership = p.add_membership(org, role=councillor[1], district=district_name)

                for key, value in contacts.items():
                    membership.add_contact_detail(key, value, "" if key == "email" else "legislature")
                yield p

        os.unlink(pdf.name)
