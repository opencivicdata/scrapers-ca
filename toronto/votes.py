from pupa.scrape import Scraper
from larvae.vote import Vote

from .utils import lxmlize

class TorontoVoteScraper(Scraper):
  def get_votes(self):
    "http://app.toronto.ca/tmmis/getAdminReport.do?function=prepareMemberVoteReport"
    "TODO"
