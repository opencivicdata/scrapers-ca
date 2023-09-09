# coding: utf-8
from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.ola.org/en/members/current/contact-information"


class OntarioPersonScraper(CanadianScraper):
    def scrape(self):
        headings = {
            "Legislative": "legislature",
            "Ministry": "office",
            "Constituency": "constituency",
        }

        page = self.lxmlize(COUNCIL_PAGE, encoding="utf-8")
        members = page.xpath('//div[@class="view-content"]//h2')

        assert len(members), "No members found"
        for member in members:
            name = member.xpath(".//a//text()")[0]
            if "Vacant seat" in name:
                continue
            url = member.xpath(".//a//@href")[0]
            node = self.lxmlize(url, encoding="utf-8")
            fax = node.xpath(
                '//div[@class="field field--name-field-fax-number field--type-string field--label-inline"]//div[@class="field__item"]//text()'
            )
            image = node.xpath(
                '//div[@class="views-element-container block block-views block-views-blockmember-member-headshot"]//img/@src'
            )

            district = ''.join(
                node.xpath(
                    '//div[@block="block-views-block-member-member-riding-block"]'
                    '//p[@class="riding"]//a//text()'
                )
            ).strip()
            nodes = node.xpath('//div[@id="main-content"]//a')
            emails = list(filter(None, [self.get_email(node, error=False) for node in nodes]))
            party = node.xpath(
                '//div[@block="block-views-block-member-current-party-block"]//div[@class="view-content"]//text()'
            )
            party = [item for item in party if item.strip()][0]

            p = Person(primary_org="legislature", name=name, district=district, role="MPP", party=party)
            p.add_source(COUNCIL_PAGE)
            p.add_source(url)
            if image:
                p.image = image[0]

            if fax:
                p.add_contact("fax", fax[-1], "legislature")

            if emails:
                p.add_contact("email", emails.pop(0))
                if emails:
                    p.extras["constituency_email"] = emails.pop(0)

            for heading, note in headings.items():
                office = node.xpath('//h3[contains(., "{}")]'.format(heading))
                if office:
                    try:
                        voice = self.get_phone(
                            office[0].xpath(
                                '../following-sibling::div[@class="views-field views-field-nothing"]'
                                '//span[@class="field-content"]'
                                '//strong[contains(text(),"Tel.")]'
                                '/following-sibling::text()[1]'
                            )[0],
                            error=False,
                        )
                    except Exception:
                        pass
                    else:
                        if voice:
                            p.add_contact("voice", voice, note)

            yield p
