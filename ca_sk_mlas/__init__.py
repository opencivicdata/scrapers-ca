from utils import CanadianJurisdiction


class Saskatchewan(CanadianJurisdiction):
  jurisdiction_id = u'ocd-jurisdiction/country:ca/province:sk/legislature'

  def _get_metadata(self):
    return {
      'name': 'Saskatchewan',
      'legislature_name': 'Saskatchewan Legislative Assembly',
      'legislature_url': 'http://www.legassembly.sk.ca/mlas/',
    }
