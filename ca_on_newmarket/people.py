from utils import CSVScraper


class NewmarketPersonScraper(CSVScraper):
    # There's no permalink to the ZIP or CSV, so we must manually upload a copy to S3. Last retrieved: 2018-11-06.
    # http://open.newmarket.ca/opendata/navigo/#/show/SQLQ6R6C_12?disp=D156E60C6F85
    csv_url = "http://represent.opennorth.ca.s3.amazonaws.com/data/2016-11-15-newmarket.csv"
    corrections = {
        "primary role": {
            "Deputy Mayor and Regional Councillor": "Deputy Mayor",
        },
    }
