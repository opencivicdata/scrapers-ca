# coding: utf8
from ca_qc_montreal import MontrealPersonScraper
from utils import CanadianJurisdiction


class RiviereDesPrairiesPointeAuxTrembles(CanadianJurisdiction):
  jurisdiction_id = u'ocd-jurisdiction/country:ca/csd:2466023/arrondissement:rivière-des-prairies-pointe-aux-trembles/council'
  ocd_division = u'ocd-division/country:ca/csd:2466023/arrondissement:rivière-des-prairies-pointe-aux-trembles'

  def _get_metadata(self):
    return {
      'name': u'Rivière-des-Prairies-Pointe-aux-Trembles',
      'legislature_name': u"Conseil d'arrondissement de Rivière-des-Prairies—Pointe-aux-Trembles",
      'legislature_url': 'http://ville.montreal.qc.ca/rdp-pat',
      'provides': ['people'],
    }

  def get_scraper(self, term, session, scraper_type):
    if scraper_type == 'people':
        return MontrealPersonScraper
