import re
from datetime import datetime

SUBCOMMITTEES = {
    # '<child match pattern>': '<parent name>',
    '^Budget Subcommittee ': 'Budget Committee',
    '^Interview Subcommittee for ': 'Civic Appointments Committee',
    '^Parks and Environment Subcommittee': 'Parks and Environment Committee',
    '^Toronto and East York Community Council ': 'Toronto and East York Community Council',
    'CDR Core Service Review Subcommittee': 'Community Development and Recreation Committee',
    'Holiday Shopping Subcommittee': 'Economic Development Committee',
    'SSO and Recycling Infrastructure Subcommittee': 'Public Works and Infrastructure Committee',
    'Seniors Strategy Subcommittee': 'Planning and Growth Management Committee',
    'Subcommittee on Establishment of Local Appeal Body': 'Planning and Growth Management Committee',
    'Subcommittee to Review Billy Bishop Airport Consultant Reports': 'Toronto and East York Community Council',
    'Tenant Issues Committee': 'Executive Committee',
    'Tenant Issues Subcommittee': 'Community Development and Recreation Committee',
}

# Taking the name from TMMIS to be the normalized name.
AGENCY_PSEUDONYMS = {
    # '<raw match pattern>': '<normalized tmmis name>',
    '^Civic Theatres Toronto$': 'Board of Directors of Civic Theatres Toronto',
    '^Property Standards Committee/Fence Viewers$': 'Property Standards Committee',
    '^Sony Centre for the Performing Arts$': 'Board of Directors of The Hummingbird (Sony) Centre for the Performing Arts',
    '^St\. Lawrence Centre for the Arts$': 'Board of Directors of the St. Lawrence Centre for the Arts',
    '^Toronto Centre for the Arts$': 'Board of Directors of the Toronto Centre for the Arts',
    '^Toronto Atmospheric Fund$': 'Board of Directors of the Toronto Atmospheric Fund',
    '^Toronto Zoo$': 'Board of Management of the Toronto Zoo',
}

PERSON_PSEUDONYMS = {
    'Mayor&nbsp John Tory': 'John Tory',
    # TODO: Add aliases?
    'Catherine/Kate': 'Kate',
    'Justin J. Di Ciano': 'Justin Di Ciano',
    'Norman Kelly': 'Norm Kelly',
    'Ming-Tat Cheung': 'Ming Tat Cheung',
    'Derek "drex" Jancar': 'Derek Jancar',
}

def regex_dict_lookup(lookup_dict, string, default_return=None):
    matches = []
    for pattern, value in lookup_dict.items():
        if re.search(pattern, string): matches.append(value)

    if len(matches) == 1:
        return matches.pop()
    elif len(matches) == 0:
        return default_return
    else:
        msg = 'Multiple regex matches for {}: {}'.format(string, matches)
        raise Exception(msg)

def normalize_whitespace(string):
    return re.sub(r'\s+', ' ', string)

def get_parent_committee(child_name):
    return regex_dict_lookup(SUBCOMMITTEES, child_name)

def format_date(milli_epoch):
    return datetime.fromtimestamp(int(milli_epoch)/1000).strftime('%Y-%m-%d')

def normalize_org_name(name):
    name = re.sub(r'sub-?committee', 'Subcommittee', name, flags=re.IGNORECASE)
    name = normalize_whitespace(name)
    name = regex_dict_lookup(AGENCY_PSEUDONYMS, name, name)

    return name

def normalize_person_name(name):
    name = normalize_whitespace(name)
    for original, replacement in PERSON_PSEUDONYMS.items():
        name = name.replace(original, replacement)

    return name
