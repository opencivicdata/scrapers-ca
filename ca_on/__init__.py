from utils import CanadianJurisdiction


class Ontario(CanadianJurisdiction):
    classification = "legislature"
    division_id = "ocd-division/country:ca/province:on"
    division_name = "Ontario"
    name = "Legislative Assembly of Ontario"
    url = "http://www.ontla.on.ca"
    parties = [
        {"name": "Green Party of Ontario"},
        {"name": "New Democratic Party of Ontario"},
        {"name": "Ontario Liberal Party"},
        {"name": "Progressive Conservative Party of Ontario"},
        {"name": "Independent"},
        {"name": "New Blue Party of Ontario"},
    ]
    skip_null_valid_from = True
    exclude_types = ["school_district"]
