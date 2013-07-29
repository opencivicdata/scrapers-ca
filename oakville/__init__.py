from pupa.scrape import Jurisdiction

# from .events import TorontoEventScraper
from .people import OakvillePersonScraper
# from .votes import TorontoVoteScraper
from .utils import lxmlize

import re

class Oakville(Jurisdiction):
  jurisdiction_id = 'ca-on-oakville'

  def get_metadata(self):
    return {
      'name': 'Oakville',
      'legislature_name': 'Oakville Town Council',
      'legislature_url': 'http://www.oakville.ca/townhall/council.html',
      'terms': [{
        'name': '2010-2014',
        'sessions': ['2010-2014'],
        'start_year': 2010,
        'end_year': 2014,
      }],
      'provides': ['people'],
      'parties': [],
      'session_details': {
        '2010-2014': {
          '_scraped_name': '2010-2014',
        }
      },
      'feature_flags': [],
      # '_ignored_scraped_sessions': ['2006-2010'],
    }

  def get_scraper(self, term, session, scraper_type):
    # if scraper_type == 'events':
    #     return TorontoEventScraper
    if scraper_type == 'people':
        return OakvillePersonScraper
    # if scraper_type == 'votes':
    #     return TorontoVoteScraper

  def scrape_session_list(self):
    page = lxmlize('http://www.oakville.ca/townhall/council.html')
    terms = page.xpath("//div[@class='colsevenfive multicol']//ul//li//a[contains(text(),'Orientation Manual')]")[0]
    terms = re.match(r'([0-9]{4})-([0-9]{4})', terms.text_content()).group()
    return [terms]
    