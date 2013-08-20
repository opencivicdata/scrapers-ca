# coding: utf8
from ca_qc_montreal import MontrealPersonScraper
from utils import CanadianJurisdiction


class SaintLeonard(CanadianJurisdiction):
  jurisdiction_id = u'ocd-jurisdiction/country:ca/csd:2466023/arrondissement:saint-léonard/council'
  ocd_division = u'ocd-division/country:ca/csd:2466023/arrondissement:saint-léonard'

  def _get_metadata(self):
    return {
      'name': u'Saint-Léonard',
      'legislature_name': u"Conseil d'arrondissement de Saint-Léonard",
      'legislature_url': 'http://ville.montreal.qc.ca/st-leonard',
      'provides': ['people'],
    }

  def get_scraper(self, term, session, scraper_type):
    if scraper_type == 'people':
        return MontrealPersonScraper
