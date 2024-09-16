import html
import re

from utils import CUSTOM_USER_AGENT, CanadianScraper
from utils import CanadianPerson as Person

COUNCIL_PAGE = "http://www.cbrm.ns.ca/mayor-council-2.html"
MAYOR_PAGE = "http://www.cbrm.ns.ca/mayor"


class CapeBretonPersonScraper(CanadianScraper):
    def scrape(self):
        def decode_email(script):
            raw_address = re.findall(r"(?<=addy).*?;\s*addy", script)
            local_part = html.unescape(raw_address[0]).split("= ", 1)[1].split(";", 1)[0]
            return re.sub(r"['\s+]", "", local_part) + "cbrm.ns.ca"

        page = self.lxmlize(COUNCIL_PAGE, user_agent=CUSTOM_USER_AGENT)

        councillors = page.xpath("//table/tbody/tr")[1:]
        assert len(councillors), "No councillors found"
        for councillor in councillors:
            name = " ".join(councillor.xpath("./td[2]//text()"))
            if "District " in name:  # Vacant
                continue
            district = "District {}".format(councillor.xpath(".//strong")[0].text_content())

            address = councillor.xpath(".//td")[2].text_content().replace("\r\n", ", ")
            contact_nodes = councillor.xpath(".//td[4]/text()")
            if ":" not in contact_nodes[0]:
                contact_nodes = councillor.xpath(".//td[4]/p/text()")

            phone = contact_nodes[0].split(":")[1]
            email_script = councillor.xpath(".//script")[0].text_content()
            email = decode_email(email_script)

            # one number had a U+00A0 in it for some reason
            phone = phone.replace("(", "").replace(")", "-").replace(" ", "").replace("\N{NO-BREAK SPACE}", "")
            if "or" in phone:  # phone and cell
                phone = phone.split("or")[0]

            clean_name = name.replace("“", '"').replace("”", '"')
            p = Person(primary_org="legislature", name=clean_name, district=district, role="Councillor")
            p.add_source(COUNCIL_PAGE)
            p.add_contact("address", address, "legislature")
            p.add_contact("voice", phone, "legislature")
            p.add_contact("email", email)

            if "F" in contact_nodes[1]:
                fax = contact_nodes[1].split(":")[1].replace("(", "").replace(")", "-").replace(" ", "")
                p.add_contact("fax", fax, "legislature")

            councillor_url = councillor.xpath(".//a/@href")[0]
            p.add_source(councillor_url)
            page = self.lxmlize(councillor_url, user_agent=CUSTOM_USER_AGENT)
            image = page.xpath(f'//img[contains(@title, "{name}")]/@src')
            if image:
                p.image = image[0]
            yield p

        mayorpage = self.lxmlize(MAYOR_PAGE, user_agent=CUSTOM_USER_AGENT)

        info = mayorpage.xpath("//div[@class='item-page']/p/text()")[1]
        name = " ".join(info.split()[:2])

        photo_url = mayorpage.xpath("//span/img/@src")[0]
        contact_nodes = mayorpage.xpath('//aside//h3[contains(text(), "Contact")]/following-sibling::div[1]')[0]
        address = contact_nodes.xpath(".//p[1]/text()")[0]
        phone = contact_nodes.xpath(".//p[2]/text()")[0].split(": ")[1]
        fax = contact_nodes.xpath(".//p[2]/text()")[1].split(": ")[1]
        email = self.get_email(contact_nodes.xpath(".//p[3]")[0])

        p = Person(primary_org="legislature", name=name, district="Cape Breton", role="Mayor")
        p.add_source(MAYOR_PAGE)
        p.add_contact("address", address, "legislature")
        p.add_contact("voice", phone, "legislature")
        p.add_contact("email", email)
        p.add_contact("fax", fax, "legislature")
        p.image = photo_url
        yield p
