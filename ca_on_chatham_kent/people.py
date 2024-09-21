import re
from collections import defaultdict

from lxml import etree

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_DATA_URL = "https://www.chatham-kent.ca/localgovernment/councillors/_vti_bin/Lists.asmx"
COUNCIL_PAGE = "https://www.chatham-kent.ca/localgovernment/councillors/Pages/Councillors-by-Ward.aspx"
MAYOR_CONTACT_PAGE = "https://www.chatham-kent.ca/localgovernment/mayor/Pages/Connect-with-the-Mayor.aspx"


class ChathamKentPersonScraper(CanadianScraper):
    def scrape(self):
        seat_numbers = defaultdict(int)

        headers = {"content-type": "text/xml"}
        body = '<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"><soap:Body><GetListItems xmlns="http://schemas.microsoft.com/sharepoint/soap/"><listName>councillorsByWard</listName><viewName></viewName><query><Query><OrderBy Override="TRUE"><FieldRef Ascending="True" Name="Title" /></OrderBy></Query></query><viewFields><ViewFields Properties="True" /></viewFields><rowLimit>50</rowLimit><queryOptions><QueryOptions></QueryOptions></queryOptions></GetListItems></soap:Body></soap:Envelope>'

        response = self.post(url=COUNCIL_DATA_URL, data=body, headers=headers)
        page = etree.fromstring(response.content)  # noqa: S320
        namespace = {"z": "#RowsetSchema", "rs": "urn:schemas-microsoft-com:rowset"}

        councillors = page.findall(".//z:row", namespace)
        assert len(councillors), "No councillors found"
        for councillor in councillors:
            title = councillor.xpath("./@ows_Title")[0]
            ward, name = re.split(r"(?<=\d)\s", title)
            name.replace("Councillor ", "")
            seat_numbers[ward] += 1
            district = f"{ward} (seat {seat_numbers[ward]})"

            url = councillor.xpath("./@ows_URL")[0].split(",")[0]
            page = self.lxmlize(url, user_agent="Mozilla/5.0")
            p = Person(primary_org="legislature", name=name, district=district, role="Councillor")
            p.add_source(COUNCIL_PAGE)
            p.add_source(url)

            p.image = page.xpath('//div[@id="mainContent"]//img/@src')[0]

            address = page.xpath("//hr/following-sibling::*")[1].text_content()
            p.add_contact("address", address, "legislature")
            email = self.get_email(page)
            p.add_contact("email", email)
            phone = self.get_phone(page)
            p.add_contact("voice", phone, "legislature")
            yield p

        page = self.lxmlize(COUNCIL_PAGE)

        mayor_url = page.xpath('//@href[contains(., "Mayor-")]')[0]
        page = self.lxmlize(mayor_url)
        contact_page = self.lxmlize(MAYOR_CONTACT_PAGE)

        name = page.xpath("//h1")[0].text_content().replace("Mayor ", "")
        image = page.xpath('//img[@style="BORDER:0px solid;"]/@src')[0]
        email = self.get_email(contact_page)
        phone = self.get_phone(contact_page)
        address = ",".join(
            contact_page.xpath('//h2[contains(., "Mailing Address")]/following-sibling::p[1]/text()')[2:]
        )

        p = Person(primary_org="legislature", name=name, district="Chatham-Kent", role="Mayor", image=image)
        p.add_contact("email", email)
        p.add_contact("voice", phone, "legislature")
        p.add_contact("address", address, "legislature")
        p.add_source(mayor_url)
        p.add_source(MAYOR_CONTACT_PAGE)

        yield p
