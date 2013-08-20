# coding: utf8
from ca_qc_montreal import MontrealPersonScraper
from utils import CanadianJurisdiction


class Lile_Bizard_Sainte_Genevieve(CanadianJurisdiction):
  jurisdiction_id = "ca-qc-l'ile-bizard-sainte-genevieve"

  def _get_metadata(self):
    return {
      'name': u"L'Île-Bizard—Sainte-Geneviève",
      'legislature_name': u"L'Île-Bizard—Sainte-Geneviève Borough Council",
      'legislature_url': 'http://depot.ville.montreal.qc.ca/bd-elus/data.json',
      'provides': ['people'],
    }

  def get_scraper(self, term, session, scraper_type):
    if scraper_type == 'people':
        return MontrealPersonScraper
