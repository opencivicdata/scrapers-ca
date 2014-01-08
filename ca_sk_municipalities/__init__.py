from utils import CanadianJurisdiction


class Saskatchewan(CanadianJurisdiction):
  jurisdiction_id = u'ocd-jurisdiction/country:ca/province:sk/legislature'

  def _get_metadata(self):
    return {
      'division_name': 'Saskatchewan',
      'name': 'Saskatchewan City Council',
      'url': 'http://www.municipal.gov.sk.ca/Programs-Services/Municipal-Directory-pdf',
    }
