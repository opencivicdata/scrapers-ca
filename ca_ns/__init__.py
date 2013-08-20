from utils import CanadianJurisdiction


class NovaScotia(CanadianJurisdiction):
  jurisdiction_id = 'ocd-jurisdiction/country:ca/province:ns/legislature'

  def _get_metadata(self):
    return {
      'name': 'Nova Scotia',
      'legislature_name': 'Nova Scotia City Council',
      'legislature_url': 'http://www.unsm.ca/doc_download/880-mayor-list-2013',
    }
