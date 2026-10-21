from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://yukonassembly.ca/members/export-mla-list"

MEMBERS = [
    ("Doris Anderson", "Porter Creek North", "Yukon Party", "867-335-2417"),
    ("Cory Bellmore", "Mayo-Tatchun", "Yukon Party", "867-393-7482"),
    ("Linda Benoit", "Whistle Bend South", "Yukon Party", "867-667-9008"),
    ("Brad Cathers", "Lake Laberge", "Yukon Party", "867-667-9059"),
    ("Yvonne Clarke", "Whistle Bend North", "Yukon Party", "867-332-0152"),
    ("Currie Dixon", "Copperbelt North", "Yukon Party", "867-393-7467"),
    ("Jen Gehmair", "Marsh Lake-Mount Lorne-Golden Horn", "Yukon Party", "867-393-7142"),
    ("Adam Gerle", "Porter Creek South", "Yukon Party", "867-335-2084"),
    ("Carmen Gustafson", "Riverdale North", "New Democratic Party", "867-393-7050"),
    ("Wade Istchenko", "Kluane", "Yukon Party", "867-393-7104"),
    ("Scott Kent", "Copperbelt South", "Yukon Party", "867-393-7104"),
    ("Ted Laking", "Porter Creek Centre", "Yukon Party", "867-393-7486"),
    ("Laura Lang", "Whitehorse West", "Yukon Party", "867-393-7492"),
    ("Brent McDonald", "Klondike", "New Democratic Party", "867-393-7050"),
    ("Patti McLeod", "Watson Lake-Ross River-Faro", "Yukon Party", "867-335-2242"),
    ("Linda Moen", "Mountainview", "New Democratic Party", "867-393-7050"),
    ("Tyler Porter", "Southern Lakes", "Yukon Party", "867-335-2087"),
    ("Debra-Leigh Reti", "Vuntut Gwitchin", "Yukon Liberal Party", "867-393-7051"),
    ("Lane Tredger", "Whitehorse Centre", "New Democratic Party", "867-393-7050"),
    ("Kate White", "Takhini", "New Democratic Party", "867-393-7001"),
    ("Justin Ziegler", "Riverdale South", "New Democratic Party", "867-393-7050"),
]


class YukonPersonScraper(CanadianScraper):
    def scrape(self):
        for name, district, party, phone in MEMBERS:
            p = Person(primary_org="legislature", name=name, district=district, role="MLA", party=party)
            p.add_source(COUNCIL_PAGE)
            p.add_contact("voice", phone, "legislature", area_code=867)
            yield p
