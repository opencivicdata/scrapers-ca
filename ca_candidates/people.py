# https://github.com/opencivicdata/scrapers-ca/blob/b19f84783efe046fac96426ebe6e1d7c8dcf1fcd/ca_candidates/people.py
import logging
import re

import requests
import scrapelib
from opencivicdata.divisions import Division
from unidecode import unidecode

from utils import CanadianPerson as Person
from utils import CanadianScraper

SOCIAL_MEDIA_DOMAINS = (
    "facebook.com",
    "instagram.com",
    "linkedin.com",
    "twitter.com",
    "x.com",
    "youtube.com",
)
CLEAN_EMAIL_REGEX = re.compile(r"mailto:|\?subject=.+")

TRANSLATION_TABLE = str.maketrans("\u2013\u2014-", "   ")
CONSECUTIVE_WHITESPACE_REGEX = re.compile(r"\s+")
DELETE_REGEX = re.compile(r"[\u200f]")
CORRECTIONS = {
    # Different names.
    "Kelowna Lake Country": "Kelowna",
    # Typographic errors.
    "Northwest Territores": "Northwest Territories",
}

logger = logging.getLogger(__name__)


class CanadaCandidatesPersonScraper(CanadianScraper):
    normalized_names = {}

    def normalize_district(self, district):
        # Ignore accents, hyphens, lettercase, and leading, trailing and consecutive whitespace.
        district = unidecode(district.translate(TRANSLATION_TABLE)).title().strip()
        district = DELETE_REGEX.sub("", CONSECUTIVE_WHITESPACE_REGEX.sub(" ", district))
        return CORRECTIONS.get(district, district)

    def scrape(self):
        # Create list mapping names to IDs.
        for division in Division.get("ocd-division/country:ca").children("ed"):
            if "2023" in division.id:
                self.normalized_names[self.normalize_district(division.name)] = division.name

        for party in (
            "liberal",
            "ndp",
            "green",
        ):
            yield from getattr(self, f"scrape_{party}")()

    def scrape_ndp(self):
        delete_regex = re.compile("[ '.-]")

        start_url = "https://www.ndp.ca/candidates"
        page = self.lxmlize(start_url)

        candidates = page.xpath('//div[@class="campaign-civics-list-items"]/div')
        assert len(candidates), "No NDP candidates found"

        for candidate in candidates:
            name = candidate.xpath("./div/div/div")[0].text_content()
            image = f'https://www.ndp.ca{candidate.xpath("./div/img")[0].get("data-img-src")}'
            district = self.normalized_names[
                self.normalize_district(candidate.xpath("./div/div/div")[1].text_content())
            ]
            p = Person(
                primary_org="lower",
                name=name,
                district=district,
                role="candidate",
                party="New Democratic Party",
                image=image,
            )

            nameclean = delete_regex.sub("", unidecode(name)).lower()
            url = f"https://{nameclean}.ndp.ca"
            if name in {
                "Julie Girard-Lemay",
                "Tommy Bureau",
                "Lise  Garon",
                "Hugues Boily-Maltais",
            }:  # these candidates have npd instead of ndp in url
                url = f"https://{nameclean}.npd.ca"
            if name == "Arlington Antonio Santiago":
                url = "https://arlingtonsantiago.ndp.ca"
            if name == "Tammy Bentz":
                url += "/contact"

            p.add_source(start_url)
            p.add_source(url)

            # e.g. "requests.exceptions.SSLError: HTTPSConnectionPool(host='nimamachouf.org', port=443)"
            try:
                candidatepage = self.lxmlize(url)

                if email := candidatepage.xpath('//a[contains(@href, "mailto:")]/@href'):
                    p.add_contact("email", CLEAN_EMAIL_REGEX.sub("", email[0]))

                for xpath in (
                    "//a[contains(@href, 'facebook') or contains(@href, 'fb')]/@href",  # Facebook
                    "//a[contains(@href, 'instagram')]/@href",  # Instagram
                    "//a[contains(@href, 'twitter')]/@href",  # Twitter
                    "//a[contains(@href, 'youtube')]/@href",  # Youtube
                ):
                    if element := candidatepage.xpath(xpath):
                        p.add_link(element[0])

                if phone := candidatepage.xpath('//a[contains(@href, "tel:")]/@href'):
                    p.add_contact("voice", phone[0].replace("tel:", ""), "office")
            except requests.RequestException:
                logger.exception()

            yield p

    def scrape_liberal(self):
        start_url = "https://liberal.ca/your-liberal-candidates/"
        page = self.lxmlize(start_url)

        candidates = page.xpath('//div[@class="person-listing-container"]/article')
        assert len(candidates), "No Liberal candidates found"

        for candidate in candidates:
            name = candidate.xpath("./div/header/h2/text()")[0]
            district = self.normalized_names[self.normalize_district(candidate.xpath("./div/header/h3/text()")[0])]

            p = Person(primary_org="lower", name=name, district=district, role="candidate", party="Liberal Party")
            # image is still a div element -> extract url

            p.add_source(start_url)

            for contact in candidate.xpath("./div/div")[1].xpath("./div/a/@href"):
                if any(domain in contact for domain in SOCIAL_MEDIA_DOMAINS):
                    p.add_link(contact)
                else:
                    candidatepage = self.lxmlize(contact)
                    if email := candidatepage.xpath('//a[contains(@href, "mailto:")]/@href'):
                        p.add_contact("email", CLEAN_EMAIL_REGEX.sub("", email[0]).replace("Canada￼", ""))

                    p.add_source(contact)

            yield p

    def scrape_green(self):
        start_url = "https://www.greenparty.ca/en/candidates/"

        candidates = []
        pattern = start_url + "page/{}"
        for page_number in range(1, 18):
            try:
                page = self.lxmlize(pattern.format(page_number))
                page_candidates = page.xpath('.//div[@class="grid-4 gpc-candidates-grid"]/article')
            except scrapelib.HTTPError:
                page_candidates = []
            if len(page_candidates):
                candidates += page_candidates

        assert len(candidates), "No Green candidates found"

        for candidate in candidates:
            name = "".join(candidate.xpath("./div/h2/a/text()"))
            district = self.normalized_names[self.normalize_district(candidate.xpath("./div/p/text()")[0])]
            image = candidate.xpath("./a/img/@src")[0]

            p = Person(
                primary_org="lower", name=name, district=district, role="candidate", party="Green Party", image=image
            )

            url = candidate.xpath("./a/@href")[0]
            p.add_source(start_url)
            p.add_source(url)

            candidatepage = self.lxmlize(url)

            for link in candidatepage.xpath(
                '//ul[@class="wp-block-social-links gpc-candidate-socials is-layout-flex wp-block-social-links-is-layout-flex"]/li/a/@href'
            ):
                if any(domain in link for domain in SOCIAL_MEDIA_DOMAINS):
                    p.add_link(link)

            if email := candidatepage.xpath('//a[contains(@href, "mailto:")]/@href'):
                p.add_contact("email", CLEAN_EMAIL_REGEX.sub("", email[0]))

            yield p
