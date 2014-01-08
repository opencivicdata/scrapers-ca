# coding: utf8
from ca_qc_montreal import MontrealPersonScraper
from utils import CanadianJurisdiction


class LIleBizardSainteGenevieve(CanadianJurisdiction):
  jurisdiction_id = u"ocd-jurisdiction/country:ca/csd:2466023/arrondissement:l~île-bizard-sainte-geneviève/council"
  ocd_division = u'ocd-division/country:ca/csd:2466023/arrondissement:l~île-bizard-sainte-geneviève'
  division_name = u"L'Île-Bizard—Sainte-Geneviève"
  name = u"Conseil d'arrondissement de L'Île-Bizard—Sainte-Geneviève"
  url = 'http://ville.montreal.qc.ca/ibsg'
  provides = ['people']

  def get_scraper(self, term, session, scraper_type):
    if scraper_type == 'people':
        return MontrealPersonScraper
