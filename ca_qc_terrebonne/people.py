from utils import CanadianScraper, CanadianPerson as Person

COUNCIL_PAGE = 'http://www.ville.terrebonne.qc.ca/fr/10/Conseil_municipal'


class TerrebonnePersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE, 'utf-8')
        councillors = page.xpath('//div[contains(@class, "member-box member-box--")]')
        assert len(councillors), 'No councillors found'
        for councillor in councillors:
            name = councillor.xpath('.//div[@class="fiche__name"]/text()')[0]
            phone = councillor.xpath('.//div[@class="fiche__social"]/span/text()')[0].split('T')[1]
            email_mailto = councillor.xpath('.//div[@class="fiche__social"]/a[contains(@href, "mailto")]/@href')
            photo_url = councillor.xpath('.//img')[0].attrib['src']

            page = self.lxmlize(councillor.xpath('.//a[@class="member-box__calltoaction"]/@href')[0])
            district = page.xpath('.//div[@class="fiche__category"]/text()')[0]


            if district == 'Maire':
                district = 'Terrebonne'
                role = 'Maire'
            else:
                district = 'District {}'.format(district)
                role = 'Conseiller'

            p = Person(primary_org='legislature', name=name, district=district, role=role, image=photo_url)
            p.add_source(COUNCIL_PAGE)
            p.add_contact('voice', phone, 'legislature')
            if email_mailto:
                email = email_mailto[0].split('mailto:')[1]
                p.add_contact('email', email)
            yield p
