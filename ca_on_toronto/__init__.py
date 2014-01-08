from utils import CanadianJurisdiction, lxmlize


class Toronto(CanadianJurisdiction):
  jurisdiction_id = u'ocd-jurisdiction/country:ca/csd:3520005/council'
  geographic_code = 3520005
  division_name = 'Toronto'
  name = 'Toronto City Council'
  url = 'http://www.toronto.ca'
  terms = [{
    'name': '2010-2014',
    'sessions': ['2010-2014'],
    'start_year': 2010,
    'end_year': 2014,
  }]
  session_details = {
    '2010-2014': {
      '_scraped_name': '2010-2014',
    }
  }
  _ignored_scraped_sessions = ['2006-2010']

  def scrape_session_list(self):
    page = lxmlize('http://app.toronto.ca/tmmis/findAgendaItem.do?function=doPrepare')
    terms = page.xpath("//select[@id='termId']//option[position()>1]/text()")
    terms.pop(0)
    return terms
