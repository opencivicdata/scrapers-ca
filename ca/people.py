import hashlib

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.ourcommons.ca/Members/en/search?caucusId=all&province=all"
COUNCIL_PAGE_MALE = "https://www.ourcommons.ca/Members/en/search?caucusId=all&province=all&gender=M"
COUNCIL_PAGE_FEMALE = "https://www.ourcommons.ca/Members/en/search?caucusId=all&province=all&gender=F"
IMAGE_PLACEHOLDER_SHA1 = ["e4060a9eeaf3b4f54e6c16f5fb8bf2c26962e15d"]


class CanadaPersonScraper(CanadianScraper):
    """
    The CSV at http://www.parl.gc.ca/Parliamentarians/en/members/export?output=CSV
    accessible from http://www.parl.gc.ca/Parliamentarians/en/members has no
    contact information or photo URLs.
    """

    def scrape(self):
        genders = {"male": COUNCIL_PAGE_MALE, "female": COUNCIL_PAGE_FEMALE}
        for gender, url in genders.items():
            page = self.lxmlize(url)
            rows = page.xpath('//div[contains(@class, "ce-mip-mp-tile-container")]')
            yield from self.scrape_people(rows, gender)

    def scrape_people(self, rows, gender):
        assert len(rows), "No members found"
        for row in rows:
            name = row.xpath('.//div[@class="ce-mip-mp-name"][1]')[0].text_content()
            constituency = row.xpath('.//div[@class="ce-mip-mp-constituency"][1]')[0].text_content()
            constituency = constituency.replace("–", "—")  # n-dash, m-dash
            if constituency == "Mont-Royal":
                constituency = "Mount Royal"

            province = row.xpath('.//div[@class="ce-mip-mp-province"][1]')[0].text_content()

            party = row.xpath('.//div[@class="ce-mip-mp-party"][1]')[0].text_content()

            url = row.xpath('.//a[@class="ce-mip-mp-tile"]/@href')[0]

            if province == "Québec":
                url = url.replace("/en/", "/fr/")

            mp_page = self.lxmlize(url)
            email = self.get_email(mp_page, '//*[@id="contact"]/div/p/a', error=False)

            photo = mp_page.xpath('.//div[@class="ce-mip-mp-profile-container"]//img/@src')[0]

            m = Person(primary_org="lower", name=name, district=constituency, role="MP", party=party)
            m.add_source(COUNCIL_PAGE)
            m.add_source(url)
            m.gender = gender
            # @see https://www.ourcommons.ca/Members/en/ziad-aboultaif(89156)
            if email:
                m.add_contact("email", email)

            if photo:
                # Determine whether the photo is actually a generic silhouette
                photo_response = self.get(photo)
                if (
                    photo_response.status_code == 200
                    and hashlib.sha1(photo_response.content).hexdigest() not in IMAGE_PLACEHOLDER_SHA1  # noqa: S324 # non-cryptographic
                ):
                    m.image = photo

            # The "Personal Web Site" section changed to "Website" some time around 2019
            personal_url = mp_page.xpath('.//a[contains(@title, "Website")]/@href')
            if personal_url:
                m.add_link(personal_url[0])

            preferred_languages = mp_page.xpath(
                './/dt[contains(., "Preferred Language")]/following-sibling::dd/text()'
            )

            if preferred_languages:
                m.extras["preferred_languages"] = [
                    language.replace("/", "").strip() for language in preferred_languages
                ]

            roles_node = mp_page.xpath('.//div[@id="roles"]')
            roles = roles_node[0].xpath('//h4[contains(., "Offices and Roles")]/following-sibling::ul[1]/li/text()')
            if roles:
                m.extras["roles"] = roles

            if province == "Québec":
                m.add_contact("address", "Chambre des communes\nOttawa ON  K1A 0A6", "legislature")
            else:
                m.add_contact("address", "House of Commons\nOttawa ON  K1A 0A6", "legislature")

            # Hill Office contacts
            # Now phone and fax are in the same element
            # <p>
            #   Telephone: xxx-xxx-xxxx<br/>
            #   Fax: xxx-xxx-xxx
            # </p>

            phone_and_fax = mp_page.xpath('.//h4[contains(., "Hill Office")]/../p')[1].xpath("./text()")

            for contact in phone_and_fax:
                contact = contact.strip()
                if "Telephone" in contact or "Téléphone" in contact:
                    phone = contact
                elif "Fax" in contact or "Télécopieur" in contact:
                    fax = contact

            if phone:
                phone = phone.replace("Telephone:", "").replace("Téléphone :", "").strip()

                if phone != "--":
                    m.add_contact("voice", phone, "legislature")

            if fax:
                fax = fax.replace("Fax:", "").replace("Télécopieur :", "").strip()

                if fax != "--":
                    m.add_contact("fax", fax, "legislature")

            # Constituency Office contacts
            # Some people has more than one, e.g. https://www.ourcommons.ca/Members/en/ben-lobb(35600)#contact
            for i, constituency_office_el in enumerate(
                mp_page.xpath('.//div[@class="ce-mip-contact-constituency-office-container"]/div')
            ):
                note = "constituency"
                if i:
                    note += f" ({i + 1})"

                address = constituency_office_el.xpath("./p[1]")[0]
                address = address.text_content().strip().splitlines()
                address = list(map(str.strip, address))
                m.add_contact("address", "\n".join(address), note)

                phone_and_fax_el = constituency_office_el.xpath(
                    './p[contains(., "Telephone")]|./p[contains(., "Téléphone")]'
                )
                if len(phone_and_fax_el):
                    phone_and_fax = phone_and_fax_el[0].text_content().strip().splitlines()
                    # Note that https://www.ourcommons.ca/Members/en/michael-barrett(102275)#contact
                    # has a empty value - "Telephone:". So the search / replace cannot include space.
                    voice = phone_and_fax[0].replace("Telephone:", "").replace("Téléphone :", "").strip()
                    if len(phone_and_fax) > 1:
                        fax = phone_and_fax[1].replace("Fax:", "").replace("Télécopieur :", "").strip()
                    
                    if voice:
                        m.add_contact("voice", voice, note)

                    if fax:
                        m.add_contact("fax", fax, note)

            yield m
