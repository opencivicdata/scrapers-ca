import re

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.leg.bc.ca/_api/search/query?querytext='(contentclass:sts_listitem%20OR%20IsDocument:True)%20SPSiteUrl:/content%20ListId:8ecafcaa-2bf9-4434-a60c-3663a9afd175%20MLAActiveOWSBOOL:1%20-LastNameOWSTEXT:Vacant'&selectproperties='Picture1OWSIMGE,Title,Path'&&sortlist='LastNameSort:ascending'&rowlimit=100&QueryTemplatePropertiesUrl='spfile://webroot/queryparametertemplate.xml'"


class BritishColumbiaPersonScraper(CanadianScraper):
    def scrape(self):
        parties = {
            "BC NDP": "New Democratic Party of British Columbia",
            "BC Liberal Party": "British Columbia Liberal Party",
        }

        page = self.lxmlize(COUNCIL_PAGE, xml=True)

        nsmap = {"d": "http://schemas.microsoft.com/ado/2007/08/dataservices"}
        members = page.xpath("//d:Cells", namespaces=nsmap)
        assert len(members), "No members found"
        for member in members:
            url = member.xpath('./d:element/d:Key[text()="Path"]/following-sibling::d:Value/text()', namespaces=nsmap)[
                0
            ]
            if "vacant" in url.lower():
                continue
            page = self.lxmlize(url)

            name = (
                page.xpath('//div[contains(@class, "BCLASS-pagetitle")]//h3/text()')[0]
                .replace("Wm.", "")
                .replace(", Q.C.", "")
                .replace(", K.C.", "")
                .strip()
            )
            district, party = cleanup_list(page.xpath('//div[@id="MinisterTitle"]/following-sibling::text()'))
            party = parties.get(party, party)
            p = Person(primary_org="legislature", name=name, district=district, role="MLA", party=party)
            p.add_source(COUNCIL_PAGE)
            p.add_source(url)

            p.image = page.xpath('//img[contains(@src, "Members")]/@src')[0]

            email = page.xpath('//div[@class="convertToEmail"]//text()')[0].strip()
            if "#" in email:
                email = email.split("#")[0]
            if email:
                p.add_contact("email", email)

            office = ", ".join(cleanup_list(page.xpath('//h4[contains(text(), "Office:")]/ancestor::div/text()')))
            office = re.sub(r"\s{2,}", " ", office)
            p.add_contact("address", office, "legislature")

            constituency = ", ".join(
                cleanup_list(page.xpath('//h4[contains(text(), "Constituency:")]/ancestor::div[1]//text()'))
            )
            constituency = re.sub(r"\s{2,}", " ", constituency).split(", Phone")[0]
            p.add_contact("address", constituency, "constituency")

            phones = cleanup_list(page.xpath('//span[contains(text(), "Phone:")]/following-sibling::text()'))

            office_phone = phones[0]
            p.add_contact("voice", office_phone, "legislature")
            if len(phones) > 1:
                constituency_phone = phones[1]
                p.add_contact("voice", constituency_phone, "constituency")

            yield p


def cleanup_list(dirty_list):
    return list(filter(None, (x.strip() for x in dirty_list)))
