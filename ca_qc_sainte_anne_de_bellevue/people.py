from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.ville.sainte-anne-de-bellevue.qc.ca/fr/199/elus-municipaux"


class SainteAnneDeBellevuePersonScraper(CanadianScraper):
    def scrape(self):
        def decode_email(e):
            de = ""
            k = int(e[:2], 16)

            for i in range(2, len(e) - 1, 2):
                de += chr(int(e[i : i + 2], 16) ^ k)

            return de

        page = self.lxmlize(COUNCIL_PAGE)

        councillors = page.xpath('//div[@class="col-md-12"]')[0]
        assert len(councillors), "No councillors found"

        roles_and_districts = councillors.xpath(".//h2/text()")
        roles = []
        districts = []
        names = []
        emails = []

        # Fill in roles and districts via h2 tags
        for role in roles_and_districts:
            role_and_district = role.split()

            roles.append(role_and_district[0])

            if len(role_and_district) == 1:
                districts.append("Sainte-Anne-de-Bellevue")
            else:
                districts.append("District " + role_and_district[2])

        # Fill in contact info via p tags.
        contact_info = councillors.xpath('.//p[a[contains(@href, "@")]]')
        for contact in contact_info:
            contact = contact.text_content().split()
            name = " ".join(contact[:2])
            names.append(name)

            email = contact[3]
            email = email.replace("Président", "")
            emails.append(email)

        assert len(roles) == len(districts) == len(names) == len(emails), "Lists are not of equal length"
        for i in range(len(roles)):
            p = Person(primary_org="legislature", name=names[i], district=districts[i], role=roles[i])
            p.add_source(COUNCIL_PAGE)
            p.add_contact("email", emails[i])
            yield p
