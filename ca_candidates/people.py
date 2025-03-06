from utils import CanadianPerson as Person
from utils import CanadianScraper

NDP_PAGE = "https://www.ndp.ca/candidates"
LIBERAL_PAGE = "https://liberal.ca/your-liberal-candidates/"
GREEN_PARTY_PAGE = "https://www.greenparty.ca/en/candidates/"

class CanadaCandidatesPersonScraper(CanadianScraper):
    def scrape(self):
        # parties being scraped
        parties = (
            'liberal',
            'ndp',
            'green',
        )
        for party in parties:
            party_method = getattr(self, f'scrape_{party}')
            yield from party_method()

    def scrape_ndp(self):
        page = self.lxmlize(NDP_PAGE)
        candidates = page.xpath('//div[@class="campaign-civics-list-items"]/div')
        assert(len(candidates))

        for candidate in candidates:
            name = candidate.xpath('./div/div/div')[0].text_content()
            image = candidate.xpath('./div/img')[0].get('data-img-src')
            image = "https://www.ndp.ca" + image
            district = candidate.xpath('./div/div/div')[1].text_content()

            p = Person(primary_org="lower", name=name, district=district, role="candidate", party="New Democratic Party", image=image)

            nameclean = name.replace(" ", "").replace("-", "").replace(".", "").replace("é", "e").replace("ô", "o").lower()
            url = "https://" + nameclean + ".ndp.ca"
            if name == "Nimâ Machouf":
                url = "https://bio.site/nimamachouf"
            if name == 'Julie Girard-Lemay' or name == 'Tommy Bureau': # these two candidates have npd instead of ndp in url
                url = "https://" + nameclean + ".npd.ca"

            
            p.add_source(NDP_PAGE)
            p.add_source(url)

            # candidate's personal page does not load
            if(name == "Dharmasena Yakandawela"):
                continue
            
            candidatepage = self.lxmlize(url)
            info = candidatepage.xpath('//div[@class="footer-column-container"]')
            if(len(info) < 2 or name == 'Hugues Boily-Maltais'): # candidate does not have contact info, doesn't exist but appears when scraping?
                continue
            elif(len(info) < 2): # candidate page formatted differently, extract contact info differently
                if name == 'Daria Juüdi-Hope':
                    continue
                elif name == 'Nimâ Machouf':
                    continue
                elif name == 'Tammy Bentz':
                    continue
                elif name == 'Bhutila Karpoche':
                    continue
                elif name == 'Samantha Green':
                    continue

            info = info[1]
            
            # getting email, phone number, social media links
            contacts = info.xpath('./ul/li/a/@href')
            # check if contacts is empty, if so it probably means they also have a phone number so query separately
            if len(contacts) == 0:
                phone_and_address = info.xpath('./div')[0]
                phone = phone_and_address.xpath('./a/@href')[0].replace("tel:", "")
                p.add_contact("voice", phone, "office")
                ptags = phone_and_address.xpath('./p')
                if len(ptags) > 1: # indicates that there is also an address present
                    address = ptags[1].text_content()
                    p.add_contact("address", address, "office")

                other = info.xpath('./div')[1]
                other = other.xpath('./ul/li/a/@href')
                for contact in other:
                    if "mailto:" in contact:
                        email = contact.replace("mailto:", "")
                        p.add_contact("email", email)
                    else:
                        p.add_link(contact)
            else: 
                for contact in contacts:
                    if "mailto:" in contact:
                        email = contact.replace("mailto:", "")
                        p.add_contact("email", email)
                    else:
                        p.add_link(contact)

            yield p

    
    def scrape_liberal(self):
        page = self.lxmlize(LIBERAL_PAGE)

        candidates = page.xpath('//div[@class="person-listing-container"]/article')
        assert(len(candidates))
        
        for candidate in candidates:
            name = candidate.xpath('./div/header/h2/text()')[0]
            district = candidate.xpath('./div/header/h3/text()')[0]
            image = candidate.xpath('./div/div')[0]

            p = Person(primary_org="lower", name=name, district=district, role="candidate", party="Liberal Party")
            # , image=image)
            # image is still a div element -> extract url

            p.add_source(LIBERAL_PAGE)

            row = candidate.xpath('./div/div')[1]
            contacts = row.xpath('./div/a/@href')
            for contact in contacts:
                if "facebook.com" in contact or "twitter.com" in contact or "instagram.com" in contact or "x.com" in contact:
                    p.add_link(contact)
                else: # candidate may have individual page with more information 
                    p.add_source(contact)
                    
            yield p
    
    def scrape_green(self):
        page1 = self.lxmlize(GREEN_PARTY_PAGE + "page/1")
        page2 = self.lxmlize(GREEN_PARTY_PAGE + "page/2")
        page3 = self.lxmlize(GREEN_PARTY_PAGE + "page/3")
        page4 = self.lxmlize(GREEN_PARTY_PAGE + "page/4")
        candidates = []
        candidates = candidates + page1.xpath('.//div[@class="grid-4 gpc-candidates-grid"]/article')
        candidates = candidates + page2.xpath('.//div[@class="grid-4 gpc-candidates-grid"]/article')
        candidates = candidates + page3.xpath('.//div[@class="grid-4 gpc-candidates-grid"]/article')
        candidates = candidates + page4.xpath('.//div[@class="grid-4 gpc-candidates-grid"]/article')
        
        for candidate in candidates:
            name = candidate.xpath('./div/h2/a/text()')
            name = "".join(name)
            district = candidate.xpath('./div/p/text()')[0]
            image = candidate.xpath('./a/img/@src')[0]
           
            p = Person(primary_org="lower", name=name, district=district, role="candidate", party="Green Party", image=image)

            url = candidate.xpath('./a/@href')[0]
            p.add_source(GREEN_PARTY_PAGE)
            p.add_source(url)

            candidatepage = self.lxmlize(url)
            links = candidatepage.xpath('//ul[@class="wp-block-social-links gpc-candidate-socials is-layout-flex wp-block-social-links-is-layout-flex"]/li/a/@href')

            for link in links:
                p.add_link(link)
            
            email = candidatepage.xpath('//a[contains(@href, "mailto:")]/@href')
            if(len(email) > 0): # some candidates do not have email
                email = email[0].replace("mailto:", "")

            yield p

