from pupa.scrape import Jurisdiction

from ca_qc_montreal import MontrealPersonScraper
from utils import lxmlize

class Villeray_Saint_Michel_Parc_Extension(Jurisdiction):
  jurisdiction_id = 'ca-qc-villeray-saint-michel-parc-extension'

  def get_metadata(self):
    return {
      'name': 'Villeray-Saint-Michel-Parc-Extension',
      'legislature_name': 'Villeray-Saint-Michel-Parc-Extension Borough Council',
      'legislature_url': 'http://depot.ville.montreal.qc.ca/bd-elus/data.json',
      'terms': [{
        'name': 'N/A',
        'sessions': ['N/A'],
      }],
      'provides': ['people'],
      'session_details': {
        'N/A': {
          '_scraped_name': 'N/A',
        }
      },
    }

  def get_scraper(self, term, session, scraper_type):
    if scraper_type == 'people':
        return MontrealPersonScraper

  def scrape_session_list(self):
    return ['N/A']
    