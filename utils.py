from pupa.scrape import Jurisdiction, Scraper
from pupa.models import Organization
import os.path

from scrapelib import urlopen
import lxml.html


class CanadianJurisdiction(Jurisdiction):
  session_details = {
    'N/A': {
      '_scraped_name': 'N/A',
    }
  }
  terms = [
    {
      'name': 'N/A',
      'sessions': ['N/A'],
      'start_year': 1900,
      'end_year': 2030,
    }
  ]

  def __init__(self):
    for scraper_type in ('bills', 'events', 'people', 'speeches', 'votes'):
      try:
        __import__(self.__module__ + '.' + scraper_type)
      except ImportError:
        pass
      else:
        self.provides.append(scraper_type)

  def get_scraper(self, term, session, scraper_type):
    if scraper_type in self.provides:
      class_name = self.__class__.__name__ + {
        'bills': 'Bill',
        'events': 'Event',
        'people': 'Person',
        'speeches': 'Speech',
        'votes': 'Vote',
      }[scraper_type] + 'Scraper'
      return getattr(__import__(self.__module__ + '.' + scraper_type, fromlist=[class_name]), class_name)

  def scrape_session_list(self):
    return ['N/A']


def lxmlize(url, encoding='utf-8'):
  entry = urlopen(url).encode(encoding)
  page = lxml.html.fromstring(entry)

  meta = page.xpath('//meta[@http-equiv="refresh"]')
  if meta:
    _, url = meta[0].attrib['content'].split('=', 1)
    return lxmlize(url, encoding)
  else:
    page.make_links_absolute(url)
    return page


class CanadianScraper(Scraper):

  def get_organization(self):
    organization = Organization(name=self.jurisdiction.name, classification='legislature', jurisdiction_id=self.jurisdiction.jurisdiction_id)
    organization.add_source(self.jurisdiction.url)
    return organization
