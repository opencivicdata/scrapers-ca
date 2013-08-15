from utils import CanadianJurisdiction

class MontrealEst(CanadianJurisdiction):
  jurisdiction_id = 'ocd-jurisdiction/country:ca/csd:2466007/council'
  geographic_code = 2466007
  def _get_metadata(self):
    return {
      'name': 'Montreal-Est',
      'legislature_name': 'Montreal-Est City Council',
      'legislature_url': 'http://ville.montreal-est.qc.ca/site2/index.php?option=com_content&view=article&id=12&Itemid=59',
    }
