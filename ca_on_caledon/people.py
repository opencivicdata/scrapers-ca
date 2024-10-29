import re

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.caledon.ca/en/government/mayor-and-council.aspx"


class CaledonPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        councillors = page.xpath('//div[@class="fbg-row lb-imageBox cm-datacontainer"]')
        assert len(councillors), "No councillors found"
        for councillor in councillors:
            try:
                district, role_name = re.split(r"(?<=\d)\s(?!.*\d)", councillor.xpath(".//a/div")[0].text_content())
                if "Regional" in role_name:
                    role = "Regional Councillor"
                    name = role_name.replace("Regional Councillor ", "")
                else:
                    role = "Councillor"
                    name = role_name.replace("Councillor ", "")
            except ValueError:  # Mayor
                name = councillor.xpath(".//a/div")[0].text_content().replace("Mayor ", "")
                district = "Caledon"
                role = "Mayor"

            url = councillor.xpath(".//@href")[0]
            page = self.lxmlize(url)

            # phone numbers populated by JS request
            contact_num = page.xpath('//div[@class="contactBody"]/div/@id')[0].replace("contactEntry_", "")
            contact_data = self.get(
                f"https://www.caledon.ca//Modules/Contact/services/GetContactHTML.ashx?isMobile=false&param={contact_num}&lang=en"
            ).text
            voice = re.findall(r"(?<=tel://)\d+(?=\">)", contact_data)

            image = councillor.xpath(".//@src")[0]

            district = district.replace("\xa0", " ")
            if "&" in district:  # Councillor for multiple wards
                wards = re.findall(r"\d", district)
                for ward_num in wards:
                    p = Person(primary_org="legislature", name=name, district=f"Ward {ward_num}", role=role)
                    if voice:
                        p.add_contact("voice", voice[0], "legislature")
                    p.image = image
                    p.add_source(COUNCIL_PAGE)
                    p.add_source(url)

                    yield p
            else:
                p = Person(primary_org="legislature", name=name, district=district, role=role)
                p.add_source(COUNCIL_PAGE)
                p.add_source(url)
                if voice:
                    p.add_contact("voice", voice[0], "legislature")
                p.image = image

                yield p
