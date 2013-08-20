# coding: utf8
from ca_qc_montreal import MontrealPersonScraper
from utils import CanadianJurisdiction


class Montreal_Nord(CanadianJurisdiction):
  jurisdiction_id = 'ca-qc-montreal-nord'

  def _get_metadata(self):
    return {
      'name': 'Montréal-Nord',
      'legislature_name': 'Montréal-Nord Borough Council',
      'legislature_url': 'http://depot.ville.montreal.qc.ca/bd-elus/data.json',
      'provides': ['people'],
    }

  def get_scraper(self, term, session, scraper_type):
    if scraper_type == 'people':
        return MontrealPersonScraper
