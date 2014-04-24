from __future__ import unicode_literals

from utils import CanadianJurisdiction


# The official government source only lists top-level officials.
# @see http://www.gov.ns.ca/snsmr/municipal/government/contact.asp
class NovaScotiaMunicipalities(CanadianJurisdiction):
  jurisdiction_id = 'ocd-jurisdiction/country:ca/province:ns/municipalities'
  geographic_code = 12
  division_name = 'Nova Scotia'
  name = 'Nova Scotia Municipalities'
  url = 'http://www.unsm.ca/doc_download/880-mayor-list-2013'
