from scrapelib import urlopen
import lxml.html

def lxmlize(url, encoding = 'utf-8'):
  entry = urlopen(url).encode(encoding)
  page = lxml.html.fromstring(entry)

  meta = page.xpath('//meta[@http-equiv="refresh"]')
  if meta:
    _, url = meta[0].attrib['content'].split('=', 1)
    return lxmlize(url, encoding)
  else:
    page.make_links_absolute(url)
    return page
