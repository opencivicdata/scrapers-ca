import datetime
import pytz
import re

from urllib.parse import parse_qs, urlparse

from .constants import COMMITTEE_LIST_TEMPLATE, TIMEZONE

def toTime(date, text_time) :
    time = datetime.datetime.strptime(text_time, '%I:%M %p')
    time = time.replace(year=date.year, month=date.month, day=date.day)
    time = pytz.timezone(TIMEZONE).localize(time)
    return time

def committees_from_sessions(self, sessions=[]):
    for session in sessions:
        term = session['identifier']
        page = self.lxmlize(COMMITTEE_LIST_TEMPLATE.format(term))
        for a in page.xpath('//table[@id="list"]//td[@class="db"]/a'):
            link = a.attrib['href']
            data = committee_from_url(self, link)
            data.update({'term': term})

            yield data


def committee_from_url(self, url=None):
    page = self.lxmlize(url)
    script_text = page.xpath('//head/script[not(@src)]/text()')[0]
    committee_name = re.search(r'var decisionBodyName = "(.*)";', script_text).group(1)
    committee_code = re.search(r'meetingRefs\.push\("[0-9]{4}\.([A-Z]{2})[0-9]+"\);', script_text).group(1)
    decision_body_id = parse_qs(urlparse(url).query)['decisionBodyId'][0]

    desc = page.xpath('//div[@id="content_container"]//div[@class="info"]/descendant::text()')
    desc = [re.sub(r' ?\r\n ?', ' ', text) for text in desc if not re.search(r'^Go to \d{4}-\d{4}', text)]
    desc = ''.join(desc).strip()

    data = {
        'name': committee_name,
        'code': committee_code,
        'info': desc,
        'source_url': url,
        'decision_body_id': decision_body_id,
    }

    return data


def build_lookup_dict(self, data_list, index_key=None):
    lookup_dict = {}
    for data in data_list:
        key = data[index_key]
        if not lookup_dict.get(key):
            lookup_dict[key] = [data]
        else:
            lookup_dict[key].append(data)

    return lookup_dict
