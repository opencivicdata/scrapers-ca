from ca_qc_montreal import MontrealPersonScraper
from utils import CanadianJurisdiction

class Villeray_Saint_Michel_Parc_Extension(CanadianJurisdiction):
  jurisdiction_id = 'ca-qc-villeray-saint-michel-parc-extension'

  def _get_metadata(self):
    return {
      'name': 'Villeray-Saint-Michel-Parc-Extension',
      'legislature_name': 'Villeray-Saint-Michel-Parc-Extension Borough Council',
      'legislature_url': 'http://depot.ville.montreal.qc.ca/bd-elus/data.json',
      'provides': ['people'],
    }

  def get_scraper(self, term, session, scraper_type):
    if scraper_type == 'people':
        return MontrealPersonScraper
