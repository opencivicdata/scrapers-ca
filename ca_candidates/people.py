import csv
import json
import re

import requests
import scrapelib
from opencivicdata.divisions import Division
from six import StringIO
from six.moves.urllib.parse import urlsplit
from unidecode import unidecode

from utils import CanadianPerson as Person
from utils import CanadianScraper

NDP_PAGE = "https://www.ndp.ca/candidates"
LIBERAL_PAGE = "https://liberal.ca/your-liberal-candidates/"
GREEN_PARTY_PAGE = "https://www.greenparty.ca/en/candidates/"
CONSERVATIVE_PAGE = "https://www.conservative.ca/candidates/"


class CanadaCandidatesPersonScraper(CanadianScraper):
    normalized_names = {}

    def normalize_district(self, district):
        # Add any other one-to-one character swaps here.
        translation_table = str.maketrans("\u2013\u2014", "——")
        # Add any other characters to delete here.
        delete_regex = re.compile(r"(?<= )-|-(?= )[\u200f]")
        return delete_regex.sub("", unidecode(district.translate(translation_table)).title().strip())

    def scrape(self):
        # Create list mapping names to IDs.
        for division in Division.get("ocd-division/country:ca").children("ed"):
            if "2023" in division.id:
                self.normalized_names[self.normalize_district(division.name).replace("--", "-")] = division.name

        representatives = json.loads(
            self.get("http://represent.opennorth.ca/representatives/house-of-commons/?limit=0").text
        )["objects"]
        self.incumbents = [representative["name"] for representative in representatives]

        boundaries = json.loads(
            self.get("http://represent.opennorth.ca/boundaries/federal-electoral-districts/?limit=0").text
        )["objects"]
        boundary_name_to_boundary_id = {boundary["name"].lower(): boundary["external_id"] for boundary in boundaries}

        crowdsourcing = {}
        url = "https://docs.google.com/spreadsheets/d/1g0yaE3dr8N7pF2K9TSp2VApJHmHDyGMqH6-Ba5SQLts/export?format=csv&id=1g0yaE3dr8N7pF2K9TSp2VApJHmHDyGMqH6-Ba5SQLts"

        response = requests.get(url)
        response.encoding = "utf-8"

        key = ""

        for row in csv.DictReader(StringIO(response.text)):
            if "District Number" in row:
                boundary_id = row["District Number"]
                if not re.search(r"\A\d{5}\Z", boundary_id):
                    boundary_id = boundary_name_to_boundary_id[boundary_id.lower()]
                key = "{}/{}/{}".format(row["Party name"], boundary_id, row["Name"])

                if crowdsourcing.get(key):
                    self.warning(f"{key} already exists")
                else:
                    if row["Gender"] == "M":
                        gender = "male"
                    elif row["Gender"] == "F":
                        gender = "female"
                    else:
                        gender = None

                    crowdsourcing[key] = {
                        "gender": gender,
                        "email": row["Email"],
                        "image": row["Photo URL"],
                        "facebook": row["Facebook"],
                        "instagram": row["Instagram"],
                        "twitter": row["Twitter"],
                        "linkedin": row["LinkedIn"],
                        "youtube": row["YouTube"],
                    }

            steps = {
                "gender": (
                    lambda p: p.gender,
                    lambda p, value: setattr(p, "gender", value),
                ),
                "email": (
                    lambda p: next(
                        (
                            contact_detail["value"]
                            for contact_detail in p._related[0].contact_details
                            if contact_detail["type"] == "email"
                        ),
                        None,
                    ),
                    lambda p, value: p.add_contact("email", value),
                ),
                "image": (
                    lambda p: p.image,
                    lambda p, value: setattr(p, "image", value),
                ),
            }

        # parties being scraped
        parties = (
            # "liberal",
            # "ndp",
            # "green",
            "conservative",
        )

        for party in parties:
            party_method = getattr(self, f"scrape_{party}")
            for method in party_method():
                p = method
                if crowdsourcing.get(key):
                    o = crowdsourcing[key]

                    links = {}
                    for link in p.links:
                        domain = ".".join(urlsplit(link["url"]).netloc.split(".")[-2:])
                        if domain in ("facebook.com", "fb.com"):
                            links["facebook"] = link["url"]
                        elif domain == "instagram.com":
                            links["instagram"] = link["url"]
                        elif domain == "linkedin.com":
                            links["linkedin"] = link["url"]
                        elif domain == "twitter.com":
                            links["twitter"] = link["url"]
                        elif domain == "youtube.com":
                            links["youtube"] = link["url"]

                    for prop, (getter, setter) in steps.items():
                        if o[prop]:
                            if prop == "email" and ".gc.ca" in o[prop]:
                                self.info(f"{key}: skipping email = {o[prop]}")
                            else:
                                scraped = getter(p)
                                if not scraped:
                                    setter(p, o[prop])
                                    self.debug(f"{key}: adding {prop} = {o[prop]}")
                                elif scraped.lower() != o[prop].lower() and prop != "image":
                                    self.warning(f"{key}: expected {prop} to be {scraped}, not {o[prop]}")

                    for prop in ["facebook", "instagram", "linkedin", "twitter", "youtube"]:
                        if o[prop]:
                            scraped = links.get(prop)
                            entered = re.sub(
                                r"/timeline/\Z|\?(f?ref|lang|notif_t)=.+|\?_rdr\Z",
                                "",
                                o[prop].replace("@", "").replace("http://twitter.com/", "https://twitter.com/"),
                            )  # Facebook, Twitter
                            if not scraped:
                                p.add_link(entered)
                                self.debug(f"{key}: adding {prop} = {entered}")
                            elif scraped.lower() != entered.lower():
                                self.warning(f"{key}: expected {prop} to be {scraped}, not {entered}")
                yield p

    def scrape_ndp(self):
        page = self.lxmlize(NDP_PAGE)
        candidates = page.xpath('//div[@class="campaign-civics-list-items"]/div')
        assert len(candidates)

        for candidate in candidates:
            name = candidate.xpath("./div/div/div")[0].text_content()
            image = candidate.xpath("./div/img")[0].get("data-img-src")
            image = "https://www.ndp.ca" + image
            district = candidate.xpath("./div/div/div")[1].text_content()
            district = self.normalize_district(district).replace("--", "-")
            if district == "Hochelaga-Rosemont Est":
                district = "Hochelaga-Rosemont-Est"
            if district == "Northwest Territores":
                district = "Northwest Territories"
            d = self.normalized_names[district]
            p = Person(
                primary_org="lower",
                name=name,
                district=d,
                role="candidate",
                party="New Democratic Party",
                image=image,
            )

            nameclean = (
                name.replace(" ", "")
                .replace("-", "")
                .replace(".", "")
                .replace("é", "e")
                .replace("ô", "o")
                .replace("ü", "u")
                .lower()
            )
            url = "https://" + nameclean + ".ndp.ca"
            if name in {
                "Julie Girard-Lemay",
                "Tommy Bureau",
                "Lise  Garon",
                "Hugues Boily-Maltais",
            }:  # these candidates have npd instead of ndp in url
                url = "https://" + nameclean + ".npd.ca"
            if name == "Arlington Antonio Santiago":
                url = "https://arlingtonsantiago.ndp.ca"
            if name == "Tammy Bentz":
                url = url + "/contact"

            p.add_source(NDP_PAGE)
            p.add_source(url)

            candidatepage = self.lxmlize(url)

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
        assert len(candidates)

        for candidate in candidates:
            name = candidate.xpath("./div/header/h2/text()")[0]
            district = (
                candidate.xpath("./div/header/h3/text()")[0]
                .replace("- ", "—")
                .replace(" – ", "—")
                .replace("–", "—")
                .replace("\u200f", "")
                .replace("\u2013", "-")
                .replace("\u2014", "-")
                .strip()
            )
            district = self.normalize_district(district)
            if district == "Surrey-Newton":
                district = "Surrey Newton"
            d = self.normalized_names[district]
            if d == "Mont-Saint-Bruno—L’Acadie":
                d = "24049"
            p = Person(primary_org="lower", name=name, district=d, role="candidate", party="Liberal Party")
            # , image=image)
            # image is still a div element -> extract url

            p.add_source(LIBERAL_PAGE)

            row = candidate.xpath("./div/div")[1]
            contacts = row.xpath("./div/a/@href")
            for contact in contacts:
                if (
                    "facebook.com" in contact
                    or "twitter.com" in contact
                    or "instagram.com" in contact
                    or "x.com" in contact
                    or "linkedin.com" in contact
                    or "youtube.com" in contact
                ):
                    p.add_link(contact)
                else:
                    candidatepage = self.lxmlize(contact)
                    email = candidatepage.xpath('//a[contains(@href, "mailto:")]/@href')
                    if email != []:
                        email = email[0].replace("mailto:", "")
                        if email == "info@johngoheenliberal.ca?subject=I%20want%20to%20volunteer":  # prone to error
                            email = "info@johngoheenliberal.ca"
                        elif email == "connect@wadechang.ca?subject=Hi%20Wade%2C%20this%20is%20...":
                            email = "connect@wadechang.ca"
                        email = email.replace("Canada￼", "")

                        p.add_contact("email", email)
                    p.add_source(contact)

            yield p

    def scrape_green(self):
        candidates = []
        pattern = GREEN_PARTY_PAGE + "page/{}"
        for page_number in range(1, 17):
            try:
                page = self.lxmlize(pattern.format(page_number))
                page_candidates = page.xpath('.//div[@class="grid-4 gpc-candidates-grid"]/article')
            except scrapelib.HTTPError:
                page_candidates = []
            if len(page_candidates):
                candidates = candidates + page_candidates

        if not len(candidates):
            raise Exception("Green party returns no candidates")

        for candidate in candidates:
            name = candidate.xpath("./div/h2/a/text()")
            name = "".join(name)
            district = (
                candidate.xpath("./div/p/text()")[0]
                .replace("- ", "—")
                .replace(" – ", "—")
                .replace("–", "—")
                .replace("\u200f", "")
                .replace("\u2013", "-")
                .strip()
            )
            district = self.normalize_district(district).replace("--", "-")
            if district == "Quebec-Centre":
                district = "Quebec Centre"
            elif district == "Kelowna-Lake Country":
                district = "Kelowna"
            d = self.normalized_names[district]
            image = candidate.xpath("./a/img/@src")[0]

            p = Person(primary_org="lower", name=name, district=d, role="candidate", party="Green Party", image=image)

            url = candidate.xpath("./a/@href")[0]
            p.add_source(GREEN_PARTY_PAGE)
            p.add_source(url)

            candidatepage = self.lxmlize(url)
            links = candidatepage.xpath(
                '//ul[@class="wp-block-social-links gpc-candidate-socials is-layout-flex wp-block-social-links-is-layout-flex"]/li/a/@href'
            )

            for link in links:
                if (
                    "facebook.com" in link
                    or "twitter.com" in link
                    or "instagram.com" in link
                    or "x.com" in link
                    or "linkedin.com" in link
                    or "youtube.com" in link
                ):
                    p.add_link(link)

            email = candidatepage.xpath('//a[contains(@href, "mailto:")]/@href')
            if len(email) > 0:  # some candidates do not have email
                email = email[0].replace("mailto:", "")
                p.add_contact("email", email)

            yield p

    def scrape_conservative(self):
        page = self.lxmlize(CONSERVATIVE_PAGE)

        candidates = page.xpath('//div[@class="candidate-grid"]/div')
        assert len(candidates)

        for candidate in candidates:
            name_el = candidate.xpath("./div/div/h3/text()")
            name = ""
            for el in name_el:
                el = el.strip()
                name = name + el + " "
            name = name.strip()
            district = candidate.xpath("./div/div/p/text()")[0]
            district = self.normalize_district(district).replace("--", "-")
            if district == "Coquitlam - Port Coquitlam":
                district = "Coquitlam-Port Coquitlam"
            if district == "Mississauga  Lakeshore":
                district = "Mississauga-Lakeshore"
            if district == "Cote-Du-Sud-Riviere-Du-Loup-Kataskomiq-Temiscouata":
                district = "Cote-Du-Sud-Riviere-Du-Loup- Kataskomiq-Temiscouata"
            d = self.normalized_names[district]
            if d == "Mont-Saint-Bruno—L’Acadie":
                d = "24049"
            if district == "Megantic-L'Erable-Lotbiniere":
                d = "24046"

            p = Person(primary_org="lower", name=name, district=d, role="candidate", party="Conservative Party")
            url = candidate.xpath("./div/a/@href")
            if url:
                url = url[0]
                p.add_source(url)

                try:
                    candidatepage = self.lxmlize(url)
                    email = self.get_email(candidatepage)
                    if email:
                        p.add_contact("email", email)
                    phone = self.get_phone(candidatepage).replace("https://", "")
                    if phone:
                        p.add_contact("voice", phone, "office")

                except Exception as e:
                    continue

            p.add_source(CONSERVATIVE_PAGE)

            socials = candidate.xpath("./div/ul/li/a/@href")
            for social in socials:
                if (
                    "facebook.com" in social
                    or "twitter.com" in social
                    or "instagram.com" in social
                    or "x.com" in social
                    or "linkedin.com" in social
                    or "youtube.com" in social
                ):
                    p.add_link(social)
            yield p
