from utils import CanadianJurisdiction


# The official government source only lists top-level officials.
# @see http://www.gov.ns.ca/snsmr/municipal/government/contact.asp
class NovaScotia(CanadianJurisdiction):
  jurisdiction_id = u'ocd-jurisdiction/country:ca/province:ns/legislature'

  def _get_metadata(self):
    return {
      'division_name': 'Nova Scotia',
      'name': 'Nova Scotia City Council',
      'url': 'http://www.unsm.ca/doc_download/880-mayor-list-2013',
    }
