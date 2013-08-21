from utils import CanadianJurisdiction


class SaintJeanSurRichelieu(CanadianJurisdiction):
  jurisdiction_id = 'ocd-jurisdiction/country:ca/csd:2456083/council'
  geographic_code = 2456083

  def _get_metadata(self):
    return {
      'name': 'Saint-Jean-sur-Richelieu',
      'legislature_name': 'Conseil municipal de Saint-Jean-sur-Richelieu',
      'legislature_url': 'http://www.ville.saint-jean-sur-richelieu.qc.ca',
    }
