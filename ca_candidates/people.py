# https://github.com/opencivicdata/scrapers-ca/blob/b19f84783efe046fac96426ebe6e1d7c8dcf1fcd/ca_candidates/people.py
import logging
import re

import lxml.etree
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
    "Nonafot Nunavut": "Nunavut",
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

    def get_district(self, district):
        try:
            return self.normalized_names[self.normalize_district(district)]
        except KeyError:
            logger.exception("")

    def scrape(self):
        # Create list mapping names to IDs.
        for division in Division.get("ocd-division/country:ca").children("ed"):
            if "2023" in division.id:
                self.normalized_names[self.normalize_district(division.name)] = division.name
                self.normalized_names[self.normalize_district(division.attrs["name_fr"])] = division.name

        for party in (
            "liberal",
            "ndp",
            "green",
            "conservative",
        ):
            try:
                yield from getattr(self, f"scrape_{party}")()
            except IndexError:
                logger.exception("")

    def scrape_ndp(self):
        delete_regex = re.compile("[ '.-]")

        start_url = "https://www.ndp.ca/candidates"
        page = self.lxmlize(start_url)

        candidates = page.xpath('//div[@class="campaign-civics-list-items"]/div')
        assert len(candidates), "No NDP candidates found"

        for candidate in candidates:
            district = self.get_district(candidate.xpath("./div/div/div")[1].text_content())
            if district is None:
                continue

            name = candidate.xpath("./div/div/div")[0].text_content()
            image = f'https://www.ndp.ca{candidate.xpath("./div/img")[0].get("data-img-src")}'

            p = Person(
                primary_org="lower",
                name=name,
                district=district,
                role="candidate",
                party="New Democratic Party",
                image=image,
            )

            subdomain = delete_regex.sub("", unidecode(name).lower())
            if subdomain == "arlingtonantoniosantiago":
                subdomain = "arlingtonsantiago"

            if subdomain == "tammybentz":
                url = f"https://{subdomain}.ndp.ca/contact"
            elif subdomain in {
                "huguesboilymaltais",
                "juliegirardlemay",
                "lisegaron",
                "tommybureau",
            }:
                url = f"https://{subdomain}.npd.ca"
            else:
                url = f"https://{subdomain}.ndp.ca"

            p.add_source(start_url)
            p.add_source(url)

            try:
                candidatepage = self.lxmlize(url)

                if email := candidatepage.xpath('//a[contains(@href, "mailto:")]/@href'):
                    p.add_contact("email", CLEAN_EMAIL_REGEX.sub("", email[0]))

                for xpath in (
                    "//a[contains(@href, 'facebook') or contains(@href, 'fb')]/@href",
                    "//a[contains(@href, 'instagram')]/@href",
                    "//a[contains(@href, 'twitter')]/@href",
                    "//a[contains(@href, 'youtube')]/@href",
                ):
                    if element := candidatepage.xpath(xpath):
                        p.add_link(element[0])

                if phone := candidatepage.xpath('//a[contains(@href, "tel:")]/@href'):
                    p.add_contact("voice", phone[0].replace("tel:", ""), "office")
            except (lxml.etree.ParserError, requests.RequestException):
                # requests.exceptions.SSLError: HTTPSConnectionPool(host='nimamachouf.org', port=443)
                # lxml.etree.ParserError: Document is empty https://avilewis.ndp.ca
                logger.exception("")

            yield p

    def scrape_liberal(self):
        start_url = "https://liberal.ca/your-liberal-candidates/"
        page = self.lxmlize(start_url)

        candidates = page.xpath('//div[@class="person-listing-container"]/article')
        assert len(candidates), "No Liberal candidates found"

        for candidate in candidates:
            district = self.get_district(candidate.xpath(".//h3[contains(@class, 'person__riding-name')]/text()")[0])
            if district is None:
                continue

            name = candidate.xpath(".//h2[contains(@class, 'person__name')]/text()")[0]
            # Liberal party has got the wrong name here as of 27.3.25
            if name == "Ron Thiering" and district == "Edmonton Strathcona":
                continue

            p = Person(primary_org="lower", name=name, district=district, role="candidate", party="Liberal Party")
            # image is still a div element -> extract url

            p.add_source(start_url)

            for link in candidate.xpath(".//div[contains(@class, 'person__link-row-container')]")[0].xpath(
                "./div/a/@href"
            ):
                if any(domain in link for domain in SOCIAL_MEDIA_DOMAINS):
                    p.add_link(link)
                else:
                    try:
                        candidatepage = self.lxmlize(link)
                        if email := candidatepage.xpath('//a[contains(@href, "mailto:")]/@href'):
                            p.add_contact("email", CLEAN_EMAIL_REGEX.sub("", email[0]).replace("Canada￼", ""))

                        p.add_source(link)
                    except (
                        lxml.etree.ParserError,
                        requests.RequestException,
                        requests.exceptions.ConnectionError,
                        scrapelib.HTTPError,
                    ) as e:
                        logger.warning("%s (%s)", e, link)

            yield p

    def scrape_green(self):
        start_url = "https://www.greenparty.ca/en/candidates/"

        candidates = []
        for page_number in range(1, 343 // 20 + 1):  # 343 divisions, 20 candidates per page
            url = f"{start_url}page/{page_number}"
            try:
                page = self.lxmlize(url)
            except scrapelib.HTTPError as e:
                logger.warning("%s (%s)", e, url)
            else:
                candidates += page.xpath('.//div[@class="grid-4 gpc-candidates-grid"]/article')

        assert len(candidates), "No Green candidates found"

        for candidate in candidates:
            district = self.get_district(candidate.xpath("./div/p/text()")[0])
            if district is None:
                continue

            name = "".join(candidate.xpath("./div/h2/a/text()"))
            image = candidate.xpath("./a/img/@src")[0]

            p = Person(
                primary_org="lower", name=name, district=district, role="candidate", party="Green Party", image=image
            )

            url = candidate.xpath("./a/@href")[0]
            p.add_source(start_url)
            p.add_source(url)

            candidatepage = self.lxmlize(url)

            if email := candidatepage.xpath('//a[contains(@href, "mailto:")]/@href'):
                p.add_contact("email", CLEAN_EMAIL_REGEX.sub("", email[0]))

            for link in candidatepage.xpath(
                '//ul[@class="wp-block-social-links gpc-candidate-socials is-layout-flex wp-block-social-links-is-layout-flex"]/li/a/@href'
            ):
                if any(domain in link for domain in SOCIAL_MEDIA_DOMAINS):
                    p.add_link(link)

            yield p

    def scrape_conservative(self):
        start_url = "https://www.conservative.ca/candidates"
        page = self.lxmlize(start_url)

        candidates = page.xpath('//div[@class="candidate-grid"]/div')
        assert len(candidates)

        for candidate in candidates:
            name = " ".join(candidate.xpath("./div/div/h3/text()"))
            name = CONSECUTIVE_WHITESPACE_REGEX.sub(" ", name)
            district = self.get_district(candidate.xpath("./div/div/p")[0].text_content())
            if district is None:
                continue

            p = Person(primary_org="lower", name=name, district=district, role="candidate", party="Conservative Party")
            url = candidate.xpath("./div/a/@href")
            if url and url[0] != start_url:
                url = url[0]
                p.add_source(url)

                try:
                    candidatepage = self.lxmlize(url)
                    try:
                        email = self.get_email(candidatepage)
                    except Exception:
                        email = ""
                    if email:
                        p.add_contact("email", email)
                    try:
                        phone = self.get_phone(candidatepage).replace("https://", "").replace("%20", " ")
                    except Exception:
                        phone = ""
                    if phone:
                        p.add_contact("voice", phone, "office")

                except (
                    lxml.etree.ParserError,
                    requests.RequestException,
                    requests.exceptions.ConnectionError,
                    scrapelib.HTTPError,
                ):
                    logger.exception("")

            p.add_source(start_url)

            for link in candidate.xpath("./div/ul/li/a/@href"):
                if any(domain in link for domain in SOCIAL_MEDIA_DOMAINS):
                    p.add_link(link)
            yield p
