# coding: utf-8
import json
import re

from utils import CUSTOM_USER_AGENT
from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.assembly.nl.ca/js/members-index.js"

PARTIES = {
    "Progressive Conservative": "Progressive Conservative Party of Newfoundland and Labrador",
    "New Democrat": "New Democratic Party of Newfoundland and Labrador",
    "Liberal": "Liberal Party of Newfoundland and Labrador",
    "Independent/Non-Affiliated": "Independent",
}

HEADING_TYPE = {
    "Confederation Building Office:": "legislature",
    "Constituency Office:": "constituency",
}


class NewfoundlandAndLabradorPersonScraper(CanadianScraper):
    def scrape(self):
        self.user_agent = CUSTOM_USER_AGENT
        page = self.get(COUNCIL_PAGE)
        members = re.search(r"members = (\[([^\]]+)\])", page.content.decode(), re.DOTALL).groups()[
            0
        ]  # extract javascript array
        members = re.sub("<!--.+?-->", "", members)  # remove comments
        members = re.sub("<a.+?>", "", members).replace("</a>", "")  # tags
        members = members.replace('"', r"\"")  # escape double quotes
        members = members.replace("'", '"')  # replace single quotes
        members = re.sub("(name|district|party|phone|email):", r'"\1":', members)  # quote attributes
        for member in json.loads(members):
            if not member["name"].strip():
                print("Skipping blank member: {}".format(member))
                continue
            p = Person(
                primary_org="legislature",
                name=" ".join(reversed(member["name"].split(","))).strip(),
                district=member["district"]
                .replace("&apos;", "'")
                .replace(
                    " - ",
                    "\u2014",
                ),  # match messy boundary data
                role="MHA",
                party=PARTIES.get(member["party"]),
            )
            if member.get("email"):
                p.add_contact(
                    "email", member["email"].replace("@gov.nl.ca@gov.nl.ca", "@gov.nl.ca")  # seriously guys?!
                )

            p.add_source(COUNCIL_PAGE)
            phone = member["phone"].split("/")[0].replace("TBD", "").strip()
            if phone:
                p.add_contact("voice", phone, "legislature")

            yield p
