from ca_qc_montreal import MontrealPersonScraper
from utils import CanadianJurisdiction


class St_Laurent(CanadianJurisdiction):
  jurisdiction_id = 'ca-qc-st-laurent'

  def _get_metadata(self):
    return {
      'name': 'Saint-Laurent',
      'legislature_name': 'Saint-Laurent Borough Council',
      'legislature_url': 'http://depot.ville.montreal.qc.ca/bd-elus/data.json',
      'provides': ['people'],
    }

  def get_scraper(self, term, session, scraper_type):
    if scraper_type == 'people':
        return MontrealPersonScraper
