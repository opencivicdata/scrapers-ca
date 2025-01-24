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
        seen = set()

        for party in parties:
            party_method = getattr(self, f'scrape_{party}')
            for p in party_method():
                yield p

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

            nameclean = name.replace(" ", "").replace("-", "").replace(".", "").replace("é", "e").replace("ô", "o").replace("ü", "u").lower()
            url = "https://" + nameclean + ".ndp.ca"
            if name == 'Julie Girard-Lemay' or name == 'Tommy Bureau' or name == 'Lise  Garon' or name == 'Hugues Boily-Maltais': # these candidates have npd instead of ndp in url
                url = "https://" + nameclean + ".npd.ca"
            if name == 'Arlington Antonio Santiago':
                url = 'https://arlingtonsantiago.ndp.ca'
            if name == 'Tammy Bentz':
                url = url + "/contact"

            p.add_source(NDP_PAGE)
            p.add_source(url)

            candidatepage = self.lxmlize(url)
            info = candidatepage.xpath('//div[@class="footer-column-container"]')

            email_el = candidatepage.xpath('//a[contains(@href, "mailto:")]/@href')
            if email_el:
                email = email_el[0].replace("mailto:", "")
                p.add_contact("email", email)
            
            facebook_el = candidatepage.xpath('//a[contains(@href, "facebook") or contains(@href, "fb")]/@href')
            if facebook_el:
                facebook = facebook_el[0]
                p.add_link(facebook)

            instagram_el = candidatepage.xpath('//a[contains(@href, "instagram")]/@href')
            if instagram_el:
                instagram = instagram_el[0]
                p.add_link(instagram)

            twitter_el = candidatepage.xpath('//a[contains(@href, "twitter")]/@href')
            if twitter_el:
                twitter = twitter_el[0]
                p.add_link(twitter)

            youtube_el = candidatepage.xpath('//a[contains(@href, "youtube")]/@href')
            if youtube_el:
                youtube = youtube_el[0]
                p.add_link(youtube)

            phone_el = candidatepage.xpath('//a[contains(@href, "tel:")]/@href')
            if phone_el:
                phone = phone_el[0].replace("tel:", "")
                p.add_contact("voice", phone, "office")

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
                if "facebook.com" in contact or "twitter.com" in contact or "instagram.com" in contact or "x.com" in contact or "linkedin.com" in contact or "youtube.com" in contact:
                    p.add_link(contact)
                else:
                    candidatepage = self.lxmlize(contact)
                    info = candidatepage.xpath('//section[@class="sidebar2-section"]/div/a/@href')
                    email = candidatepage.xpath('//a[contains(@href, "mailto:")]/@href')
                    if not email == []:
                        email = email[0].replace("mailto:", "")
                        if email == 'info@johngoheenliberal.ca?subject=I%20want%20to%20volunteer':  # prone to error
                            email = 'info@johngoheenliberal.ca'
                        elif email == 'connect@wadechang.ca?subject=Hi%20Wade%2C%20this%20is%20...':
                            email = 'connect@wadechang.ca'
                        email = email.replace("Canada￼", "")

                        p.add_contact("email", email)
                    p.add_source(contact)
                    
            yield p
    
    def scrape_green(self):
        page1 = self.lxmlize(GREEN_PARTY_PAGE + "page/1")
        page2 = self.lxmlize(GREEN_PARTY_PAGE + "page/2")
        page3 = self.lxmlize(GREEN_PARTY_PAGE + "page/3")
        page4 = self.lxmlize(GREEN_PARTY_PAGE + "page/4")
        page5 = self.lxmlize(GREEN_PARTY_PAGE + "page/5")
        page6 = self.lxmlize(GREEN_PARTY_PAGE + "page/6")
        candidates = []
        candidates = candidates + page1.xpath('.//div[@class="grid-4 gpc-candidates-grid"]/article')
        candidates = candidates + page2.xpath('.//div[@class="grid-4 gpc-candidates-grid"]/article')
        candidates = candidates + page3.xpath('.//div[@class="grid-4 gpc-candidates-grid"]/article')
        candidates = candidates + page4.xpath('.//div[@class="grid-4 gpc-candidates-grid"]/article')
        candidates = candidates + page5.xpath('.//div[@class="grid-4 gpc-candidates-grid"]/article')
        candidates = candidates + page6.xpath('.//div[@class="grid-4 gpc-candidates-grid"]/article')
        
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
                if "facebook.com" in link or "twitter.com" in link or "instagram.com" in link or "x.com" in link or "linkedin.com" in link or "youtube.com" in link:
                    p.add_link(link)
            
            email = candidatepage.xpath('//a[contains(@href, "mailto:")]/@href')
            if(len(email) > 0): # some candidates do not have email
                email = email[0].replace("mailto:", "")
                p.add_contact("email", email)

            yield p

