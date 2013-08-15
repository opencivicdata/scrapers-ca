from pupa.scrape import Jurisdiction

from montreal import MontrealPersonScraper
from utils import lxmlize

class Cote_des_Neiges_Notre_Dame_de_Grace(Jurisdiction):
  jurisdiction_id = 'ca-qc-cote-des-neiges-notre-dame-de-grace'

  def get_metadata(self):
    return {
      'name': 'Cote-des-Neiges-Notre-Dame-de-Grace',
      'legislature_name': 'Cote-des-Neiges-Notre-Dame-de-Grace Borough Council',
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
    