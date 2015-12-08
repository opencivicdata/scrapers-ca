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

def normalize_org_name(name):
    name = re.sub(r'sub-?committee', 'Subcommittee', name, flags=re.IGNORECASE)
    name = re.sub(r'\s+', ' ', name)
    for pattern, org_name in AGENCY_PSEUDONYMS.items():
        if re.search(pattern, name): name = org_name

    return name

def normalize_person_name(name):
    name = re.sub(r'\s+', ' ', name)
    name = name.replace('Mayor&nbsp John Tory', 'John Tory')
    # TODO: Add aliases?
    name = name.replace('Catherine/Kate', 'Kate')
    name = name.replace('Justin J. Di Ciano', 'Justin Di Ciano')
    name = name.replace('Norman Kelly', 'Norm Kelly')
    name = name.replace('Ming-Tat Cheung', 'Ming Tat Cheung')
    name = name.replace('Derek "drex" Jancar', 'Derek Jancar')
    return name

def get_parent_committee(child_name):
    for pattern, parent_name in SUBCOMMITTEES.items():
        if re.search(pattern, child_name): return parent_name

def format_date(milli_epoch):
    return datetime.fromtimestamp(int(milli_epoch)/1000).strftime('%Y-%m-%d')
