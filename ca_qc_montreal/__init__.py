# coding: utf8
from .people import MontrealPersonScraper
from utils import CanadianJurisdiction


class Montreal(CanadianJurisdiction):
  jurisdiction_id = u'ocd-jurisdiction/country:ca/csd:2466023/council'
  geographic_code = 2466023
  division_name = u'Montréal'
  name = u'Conseil municipal de Montréal'
  url = 'http://www.ville.montreal.qc.ca'
  provides = ['people']

  def get_scraper(self, term, session, scraper_type):
    if scraper_type == 'people':
        return MontrealPersonScraper
