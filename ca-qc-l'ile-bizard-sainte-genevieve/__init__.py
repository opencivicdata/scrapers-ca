from pupa.scrape import Jurisdiction

from montreal import MontrealPersonScraper
from utils import lxmlize

class Lile_Bizard_Sainte_Genevieve(Jurisdiction):
  jurisdiction_id = "ca-qc-l'ile-bizard-sainte-genevieve"

  def get_metadata(self):
    return {
      'name': "L'Ile-Bizard-Sainte-Genevieve",
      'legislature_name': "L'Ile-Bizard-Sainte-Genevieve Borough Council",
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
    