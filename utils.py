from pupa.scrape import Jurisdiction

import os.path

from scrapelib import urlopen
import lxml.html


class CanadianJurisdiction(Jurisdiction):

  def get_metadata(self):
    metadata = {
      'feature_flags': [],
      'parties': [],
      'provides': [],
      'session_details': {
        'N/A': {
          '_scraped_name': 'N/A',
        }
      },
      'terms': [
        {
          'name': 'N/A',
          'sessions': ['N/A'],
          'start_year': 1900,
          'end_year': 2030,
        }
      ],
    }
    for scraper_type in ('bills', 'events', 'people', 'speeches', 'votes'):
      try:
        __import__(self.__module__ + '.' + scraper_type)
      except ImportError:
        pass
      else:
        metadata['provides'].append(scraper_type)
    metadata.update(self._get_metadata())
    return metadata

  def get_scraper(self, term, session, scraper_type):
    if scraper_type in self.metadata['provides']:
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
