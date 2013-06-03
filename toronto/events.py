from pupa.scrape import Scraper
from larvae.event import Event

from .utils import lxmlize

class TorontoEventScraper(Scraper):
  def get_events(self):
    "http://app.toronto.ca/tmmis/getAdminReport.do?function=prepareMeetingScheduleReport"
    "http://app.toronto.ca/tmmis/getAdminReport.do?function=prepareMemberAttendanceReport"
    "TODO"
