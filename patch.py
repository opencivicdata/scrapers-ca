from copy import deepcopy

import regex as re
from pupa.scrape.schemas.common import contact_details as _contact_details
from pupa.scrape.schemas.common import links as _links
from pupa.scrape.schemas.common import sources as _sources
from pupa.scrape.schemas.membership import schema as membership_schema
from pupa.scrape.schemas.organization import schema as organization_schema
from pupa.scrape.schemas.person import schema as person_schema
from pupa.utils import DatetimeValidator

# contact_details[].type must not be blank.
_contact_details["items"]["properties"]["type"]["blank"] = False
# Override CONTACT_TYPES in https://github.com/opencivicdata/python-opencivicdata-django/blob/master/opencivicdata/common.py
_contact_details["items"]["properties"]["type"]["enum"] = [
    "address",
    "cell",
    "email",
    "fax",
    "voice",
]
# contact_details[].value must not be blank.
_contact_details["items"]["properties"]["value"]["blank"] = False
# Validate the format of contact_details[].value if contact_details[].type is an email address or telephone number.
_contact_details["items"]["properties"]["value"]["conditionalPattern"] = [
    (r"\A([A-Za-z0-9._\'-]+)@(?:[A-Za-z0-9-]+\.)+[A-Za-z]{2,}\Z", lambda x: x["type"] == "email"),
    (r"\A1 \d{3} \d{3}-\d{4}(?: x\d+)?\Z", lambda x: x["type"] in ("text", "voice", "fax", "cell", "video", "pager")),
]
# Validate the format of contact_details[].note.
_contact_details["items"]["properties"]["note"]["pattern"] = (
    r"\A(?:constituency|legislature|office|residence|)(?: \(\d\))?\Z"
)
# contact_details[] must not include unexpected properties.
_contact_details["items"]["additionalProperties"] = False

# links[].url must not be blank.
_links["items"]["properties"]["url"]["blank"] = False
# Validate the format of links[].url.
_links["items"]["properties"]["url"]["pattern"] = r"\A(?:ftp|https?)://"
# links[] must not include unexpected properties.
_links["items"]["additionalProperties"] = False

# sources[].url must not be blank.
_sources["items"]["properties"]["url"]["blank"] = False
# Validate the format of sources[].url.
_sources["items"]["properties"]["url"]["pattern"] = r"\A(?:ftp|https?)://"
# sources[] must not include unexpected properties.
_sources["items"]["additionalProperties"] = False

# We must copy the subschema for each model.
membership_contact_details = deepcopy(_contact_details)
membership_links = deepcopy(_links)
organization_contact_details = deepcopy(_contact_details)
organization_links = deepcopy(_links)
person_contact_details = deepcopy(_contact_details)
person_links = deepcopy(_links)

social_re = re.compile(
    r"(?:facebook|fb|instagram|linkedin|twitter|youtube)\.com|conservative\.ca"
)  # special case: ca_candidates
facebook_re = re.compile(r"facebook\.com")
instagram_re = re.compile(r"instagram\.com")
linkedin_re = re.compile(r"linkedin\.com")
twitter_re = re.compile(r"twitter\.com")
youtube_re = re.compile(r"youtube\.com")

matchers = [
    (0, lambda x: x["type"] == "email" and x["note"] != "", "Membership has email with non-empty note"),
    (0, lambda x: x["type"] != "email" and x["note"] == "", "Membership has non-email with empty note"),
    (1, lambda x: x["type"] == "email", "Membership has many emails"),
]

matchers.extend(
    (
        1,
        lambda x, type=type, note=note: x["type"] == type and x["note"] == note,
        "Membership has contact_details with same type and note",
    )
    for type in ("address", "cell", "fax", "voice")
    for note in ("constituency", "legislature", "office", "residence")
)

# A membership should not have notes on emails, should have notes on non-emails,
# should have at most one email, and should, in most cases, have at most one of
# each combination of type and note.
membership_contact_details["maxMatchingItems"] = matchers
# A membership should not have links.
membership_links["maxItems"] = 0
# An organization should not have contact details.
organization_contact_details["maxItems"] = 0
# An organization should not have links.
organization_links["maxItems"] = 0
# A person should not have contact details.
person_contact_details["maxItems"] = 0
# A person should only have a link note for the canonical website.
person_links["items"]["properties"]["note"]["enum"] = ["", "web site"]
# A person should have, in most cases, at most one non-social media link, and
# should have at most one link per social media website.
person_links["maxMatchingItems"] = [
    (1, lambda x: not social_re.search(x["url"]), "Person has many non-social media links"),
    (1, lambda x: facebook_re.search(x["url"]), "Person has many facebook.com links"),
    (1, lambda x: instagram_re.search(x["url"]), "Person has many instagram.com links"),
    (1, lambda x: linkedin_re.search(x["url"]), "Person has many linkedin.com links"),
    (1, lambda x: twitter_re.search(x["url"]), "Person has many twitter.com links"),
    (1, lambda x: youtube_re.search(x["url"]), "Person has many youtube.com links"),
]

# memberships[].role must not be blank.
membership_schema["properties"]["role"]["blank"] = False
membership_schema["properties"]["contact_details"] = membership_contact_details
membership_schema["properties"]["links"] = membership_links

organization_schema["properties"]["contact_details"] = organization_contact_details
organization_schema["properties"]["links"] = organization_links

# Match initials, all-caps, short words, parenthesized nickname, and regular names.
name_fragment = (
    r"(?:"
    r"(?:\p{Lu}\.)+|"
    r"\p{Lu}+|"
    r"(?:Jr|Rev|Sr|St)\.|"
    r"da|de|den|der|la|van|von|"
    r'[("](?:\p{Lu}+|\p{Lu}\p{Ll}*(?:-\p{Lu}\p{Ll}*)*)[)"]|'
    r"(?:D'|d'|De|de|Des|Di|Du|L'|La|Le|Mac|Mc|O'|San|Van|Vander?|van|vanden)?\p{Lu}\p{Ll}+|"
    r"\p{Lu}\p{Ll}+Anne?|Marie\p{Lu}\p{Ll}+|"
    r"Ch'ng|Prud'homme|"
    r"D!ONNE|IsaBelle|Ya'ara"
    r")"
)

# Name components can be joined by apostrophes, hyphens or spaces.
person_schema["properties"]["name"]["pattern"] = re.compile(
    r"\A"
    r"(?!(?:Chair|Commissioner|Conseiller|Councillor|Deputy|Dr|Hon|M|Maire|Mayor|Miss|Mme|Mr|Mrs|Ms|Regional|Warden)\b)"
    r"(?:" + name_fragment + r"(?:'|-| - | )"
    r")+" + name_fragment + r"\Z"
)
person_schema["properties"]["gender"]["enum"] = ["male", "female", ""]
# @note https://github.com/opennorth/represent-canada-images checks whether an
# image resolves. Testing URLs here would slow down scraping.
person_schema["properties"]["image"]["pattern"] = r"\A(?:(?:ftp|https?)://|\Z)"
person_schema["properties"]["contact_details"] = person_contact_details
person_schema["properties"]["links"] = person_links
# district is used to disambiguate people within a jurisdiction.
person_schema["properties"]["district"] = {"type": "string", "blank": False}

organization_schema["properties"]["classification"]["enum"] += ["government"]


def validate_conditionalPattern(self, x, fieldname, schema, path, arguments=None):  # noqa: N802
    value = x.get(fieldname)
    if isinstance(value, str):
        for pattern, method in arguments:
            if method(x) and not re.search(pattern, value):
                self._error("does not match regular expression '{pattern}'", value, fieldname, pattern=pattern)


DatetimeValidator.validate_conditionalPattern = validate_conditionalPattern


def validate_maxMatchingItems(self, x, fieldname, schema, path, arguments=None):  # noqa: N802
    value = x.get(fieldname)
    if isinstance(value, list):
        for length, method, message in arguments:
            count = 0
            for v in value:
                if method(v):
                    count += 1
                if count > length:
                    self._error(message, value, fieldname)


DatetimeValidator.validate_maxMatchingItems = validate_maxMatchingItems
