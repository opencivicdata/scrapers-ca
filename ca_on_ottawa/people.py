import csv
from io import BytesIO, StringIO

import agate

from utils import CSVScraper


class OttawaPersonScraper(CSVScraper):
    # https://open.ottawa.ca/documents/ottawa::elected-officials-2022-2026/about
    csv_url = "https://www.arcgis.com/sharing/rest/content/items/a5e9dc2425274bb796d3ded47b0d7b00/data"
    fallbacks = {"district name": "ward name"}

    # Workaround for the download link not having the correct extension
    def csv_reader(self, url, delimiter=",", header=False, encoding=None, skip_rows=0, data=None, **kwargs):
        data = StringIO()
        binary = BytesIO(self.get(url).content)
        table = agate.Table.from_xls(binary)
        table.to_csv(data)
        data.seek(0)
        if skip_rows:
            for _ in range(skip_rows):
                data.readline()
        if header:
            return csv.DictReader(data, delimiter=delimiter)
        else:
            return csv.reader(data, delimiter=delimiter)
