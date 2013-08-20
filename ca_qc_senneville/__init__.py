from utils import CanadianJurisdiction


class Senneville(CanadianJurisdiction):
  jurisdiction_id = u'ocd-jurisdiction/country:ca/csd:2466127/council'
  geographic_code = 2466127

  def _get_metadata(self):
    return {
      'name': 'Senneville',
      'legislature_name': 'Conseil municipal de Senneville',
      'legislature_url': 'http://www.villagesenneville.qc.ca',
    }
