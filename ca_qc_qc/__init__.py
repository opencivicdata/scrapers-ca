from utils import CanadianJurisdiction


class Quebec_City(CanadianJurisdiction):
  jurisdiction_id = u'ocd-jurisdiction/country:ca/csd:2423027/council'
  geographic_code = 2423027

  def _get_metadata(self):
    return {
      'name': 'Quebec City',
      'legislature_name': 'Quebec City Council',
      'legislature_url': 'http://www.ville.quebec.qc.ca/apropos/vie_democratique/elus/conseil_municipal/membres.aspx',
    }
