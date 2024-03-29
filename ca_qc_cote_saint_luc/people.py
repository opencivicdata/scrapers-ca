# coding: utf-8
from utils import CUSTOM_USER_AGENT
from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://cotesaintluc.org/fr/municipalite/conseil/"


class CoteSaintLucPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE, user_agent=CUSTOM_USER_AGENT)
        councillors = page.xpath('//section[contains(@class,"avia-team-member")]')[:-1]
        assert len(councillors), "No councillors found"

        for councillor in councillors:
            name = councillor.xpath(".//h3/text()")[0]

            if councillor.xpath('.//div[contains(@class,"team-member-job-title")][contains(.,"Maire")]/text()'):
                role = "Maire"
                district = "Côte-Saint-Luc"
            else:
                role, district = councillor.xpath('.//div[contains(@class,"team-member-job-title")]/text()')[0].split(
                    ",", 1
                )
                if role == "Conseillère":
                    role = "Conseiller"

            image = councillor.xpath(".//img/@src")[0]
            twitter = councillor.xpath('.//p[contains(.,"Twitter")]/a/text()')
            web = councillor.xpath('.//p[contains(.,"Web")]/a/@href')
            blog = councillor.xpath('.//p[contains(.,"Blog")]/a/@href')

            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)

            p.add_contact("email", self.get_email(councillor))
            p.add_contact("voice", self.get_phone(councillor, area_codes=[514]), "legislature")
            p.image = image
            if twitter:
                p.add_link(twitter[0])
            if web:
                p.add_link(web[0])
            if blog:
                p.add_link(blog[0])

            yield p
