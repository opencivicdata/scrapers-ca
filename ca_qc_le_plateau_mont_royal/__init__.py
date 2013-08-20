from ca_qc_montreal import MontrealPersonScraper
from utils import CanadianJurisdiction


class Le_Plateau_Mont_Royal(CanadianJurisdiction):
  jurisdiction_id = 'ca-qc-le_plateau-mont-royal'

  def _get_metadata(self):
    return {
      'name': 'Le Plateau-Mont-Royal',
      'legislature_name': 'Le Plateau-Mont-Royal Borough Council',
      'legislature_url': 'http://depot.ville.montreal.qc.ca/bd-elus/data.json',
      'provides': ['people'],
    }

  def get_scraper(self, term, session, scraper_type):
    if scraper_type == 'people':
        return MontrealPersonScraper
