# coding: utf-8
from pupa.scrape import Scraper

from utils import lxmlize, CanadianLegislator as Legislator

import re

COUNCIL_PAGE = 'http://www.abbotsford.ca/mayorcouncil/city_council/email_mayor_and_council.htm'


class AbbotsfordPersonScraper(Scraper):

  def get_people(self):
    page = lxmlize(COUNCIL_PAGE)
    # TODO: councillor pages don't even have readily parsable names. Grrrr.

