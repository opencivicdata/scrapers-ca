from __future__ import unicode_literals

from utils import CanadianJurisdiction


# The Federation of Prince Edward Island Municipalities has the same data as the
# official government source.
# @see http://fpeim.ca/index.php?page=member_directory
class PrinceEdwardIslandMunicipalities(CanadianJurisdiction):
  jurisdiction_id = 'ocd-jurisdiction/country:ca/province:pe/municipalities'
  geographic_code = 11
  division_name = 'Prince Edward Island'
  name = 'Prince Edward Island Municipalities'
  url = 'http://www.gov.pe.ca/mapp/municipalitites.php'
