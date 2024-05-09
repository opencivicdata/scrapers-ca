from collections import defaultdict

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.rmwb.ca/en/mayor-council-and-administration/councillors.aspx"
MAYOR_PAGE = "https://www.rmwb.ca/en/mayor-council-and-administration/mayor.aspx"


class WoodBuffaloPersonScraper(CanadianScraper):
    def scrape(self):
        def intersection(list1,list2):
            list3 = [value for value in list1 if value in list2]
            return list3
        seat_numbers = defaultdict(int)

        page = self.lxmlize(COUNCIL_PAGE)

        # yield self.scrape_mayor()        

        wards = page.xpath('//div[@id="StandardOneColumnTK1_lm175"]//h2')
        assert len(wards), "No wards found"
        for ward in wards:
            area = ward.text_content().split("–", 1)[1].strip()
            councillors1 = ward.xpath('./following-sibling::table/tbody')
            councillors2 = ward.xpath('./following-sibling::h2[1]/preceding-sibling::table/tbody')
            if councillors2:
                councillors = intersection(councillors1,councillors2)
            else:
                councillors = councillors1

            if ward == "Ward 1":
                assert len(councillors) == 6, "Wrong number of ward 1 councillors"
            elif ward == "Ward 2":
                assert len(councillors) == 2, "Wrong number of ward 2 councillors"
            elif ward == "Ward 3":
                assert len(councillors) == 1, "Wrong number of ward 3 councillors"                

            assert len(councillors), "No councillors found for {}".format(area)

            
            for index,councillor in enumerate(councillors):
                name = councillor.xpath('.//h3')[index].text_content()

                if area in ("Ward 1", "Ward 2"):
                    seat_numbers[area] += 1
                    district = "{} (seat {})".format(area, seat_numbers[area])
                else:
                    district = area

                p = Person(primary_org="legislature", name=name, district=district, role="Councillor")
                p.add_source(COUNCIL_PAGE)

                p.image = councillor.xpath('.//img/@src')[0]

                email = self.get_email(councillor)
                p.add_contact("email", email)

                yield p

        # def scrape_mayor(self):
        #     page = self.lxmlize(MAYOR_PAGE)
        #     name = page.xpath('//h1[@id="pagetitle"]/text()')[0].replace("Mayor", "").strip()
        #     image = page.xpath('//div[@id="content"]//@src')[0]

        #     p = Person(primary_org="legislature", name=name, district="Wood Buffalo", role="Mayor")
        #     p.add_source(MAYOR_PAGE)

        #     p.image = image
        #     p.add_contact("voice", self.get_phone(page.xpath('//div[@id="icon5"]')[0]), "legislature")
        #     p.add_contact("email", "mayor@rmwb.ca")

        #     return p
