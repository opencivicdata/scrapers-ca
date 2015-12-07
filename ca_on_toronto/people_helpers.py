import re

SUBCOMMITTEES = {
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

def normalize_committee_name(name):
    name = re.sub(r'sub-?committee', 'Subcommittee', name,  flags=re.IGNORECASE)
    name = re.sub(r'\s+', ' ', name)
    return name

def get_parent_committee(child_name):
    for pattern, parent_name in SUBCOMMITTEES.items():
        if re.search(pattern, child_name): return parent_name
