from pupa.scrape import Jurisdiction

from .events import TorontoEventScraper
from .people import TorontoPersonScraper
from .votes import TorontoVoteScraper
from utils import lxmlize

class Toronto(Jurisdiction):
  jurisdiction_id = 'ca-on-toronto'
  geo_code = 4819006
  def get_metadata(self):
    return {
      'name': 'Toronto',
      'legislature_name': 'Toronto City Council',
      'legislature_url': 'http://www.toronto.ca/city_hall/index.htm',
      'terms': [{
        'name': '2010-2014',
        'sessions': ['2010-2014'],
        'start_year': 2010,
        'end_year': 2014,
      }],
      'provides': ['events', 'people', 'votes'],
      'parties': [],
      'session_details': {
        '2010-2014': {
          '_scraped_name': '2010-2014',
        }
      },
      'feature_flags': [],
      '_ignored_scraped_sessions': ['2006-2010'],
    }

  def get_scraper(self, term, session, scraper_type):
    if scraper_type == 'events':
        return TorontoEventScraper
    if scraper_type == 'people':
        return TorontoPersonScraper
    if scraper_type == 'votes':
        return TorontoVoteScraper

  def scrape_session_list(self):
    page = lxmlize('http://app.toronto.ca/tmmis/findAgendaItem.do?function=doPrepare')
    terms = page.xpath("//select[@id='termId']//option[position()>1]/text()")
    terms.pop(0)
    return terms
    