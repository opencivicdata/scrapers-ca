from ca_on_toronto.bills import TorontoBillScraper
import datetime


class TorontoIncrementalBillScraper(TorontoBillScraper):
    start_date = datetime.datetime.today() - datetime.timedelta(days=7)
