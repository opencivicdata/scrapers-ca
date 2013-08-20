from utils import CanadianJurisdiction


class NewfoundlandAndLabrador(CanadianJurisdiction):
  jurisdiction_id = 'ocd-jurisdiction/country:ca/province:nl/legislature'

  def _get_metadata(self):
    return {
      'name': 'Newfoundland Labrador',
      'legislature_name': 'Newfoundland Labrador Municipal Council',
      'legislature_url': 'http://www.ma.gov.nl.ca/ma/municipal_directory/index.html',
    }
