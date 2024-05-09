from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.strathcona.ca/council-county/mayor-council/councillors/"
MAYOR_PAGE = "https://www.strathcona.ca/council-county/mayor-council/mayor/"

class StrathconaCountyPersonScraper(CanadianScraper):
    def scrape(self):
        def councillor_scraper(self,url):
            page = self.lxmlize(url)
            name_district = page.xpath('//h1[@id="title"]')[0].text_content().replace("Councillor","").strip()
            hyphen = name_district.find("- Ward")
            name = name_district[:hyphen].strip()
            district = name_district[hyphen:].replace("-","").strip()
            email = self.get_email(page)
            phone = self.get_phone(page)
            photo = page.xpath('//img/@src')[0]
            address_block = page.xpath('//div[contains(@class,"lf-dept-contact uk-margin-medium")]/p[not(a)]')[0].text_content()
            address_lines = address_block.split("\n")
            for index,line in enumerate(address_lines):
                if line.endswith(":"):
                    address = " ".join(address_lines[index+1:index+4])
                    break
            p = Person(primary_org="legislature", name=name, role = "Councillor", district=district)
            p.image = photo
            p.add_source(COUNCIL_PAGE)
            p.add_source(url)
            p.add_contact("email", email)
            p.add_contact("voice", phone, "legislature")
            p.add_contact("address", address, "legislature")

            return p
            
        def mayor_scraper(self):
            page = self.lxmlize(MAYOR_PAGE)
            name = page.xpath('//h1[@id="title"]')[0].text_content().replace("Mayor -","").strip()
            photo = page.xpath('//img/@src')[0]
            email = self.get_email(page)
            phone = self.get_phone(page)
            address_block = page.xpath('//div[contains(@class,"lf-dept-contact uk-margin-medium")]/p[not(a)]')[0].text_content()
            address_lines = address_block.split("\n")
            for index,line in enumerate(address_lines):
                if line.endswith(":"):
                    address = " ".join(address_lines[index+1:index+4])
                    break

            p = Person(primary_org="legislature", name=name, role = "Mayor", district = "Strathcona County")
            p.image = photo
            p.add_source(MAYOR_PAGE)
            p.add_contact("email",email)
            p.add_contact("voice", phone, "legislature")
            p.add_contact("address", address, "legislature")
            
            return p
        
        page = self.lxmlize(COUNCIL_PAGE)
        councillors = page.xpath('//div[contains(@class, "uk-visible@s")]//div[@class="uk-section-muted uk-card-body"]/p/a')
        for councillor in councillors:
            url = councillor.xpath('./@href')[0]
            yield councillor_scraper(self,url)    
        
        yield mayor_scraper(self)
