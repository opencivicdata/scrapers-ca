# Canadian Legislative Scrapers 

[Pupa](https://github.com/opencivicdata/pupa) scrapers to collect Canadian legislative data at all three levels of government.

## Directory layout

- `ca` Federal module
- `ca_candidates`: Federal elections module
- `ca_{province abbreviation}`: Provincial module, like `ca_ab`
- `ca_{province abbreviation}_candidates`: Provincial elections module
- `ca_{province abbreviation}_{municipality}`: Municipal module, like `ca_ab_calgary`
- `disabled`: Disabled modules
- `docker`: Documentation and files to develop using Docker locally

## Usage

Follow the instructions in the [Python Quick Start Guide](https://github.com/opennorth/wiki/wiki/Python-Quick-Start%3A-OS-X) to install Homebrew, Git, PostGIS, Python 3.3+ and virtualenv.

```
mkvirtualenv scrapers-ca --python=`which python3`
git clone https://github.com/opencivicdata/scrapers-ca.git
cd scrapers-ca
pip install -r requirements.txt
```

Initialize the database:

```
createdb pupa
psql pupa -c "CREATE EXTENSION postgis;"
pupa dbinit ca
```

If you get an error like "no password supplied", then you need to configure the default `DATABASE_URL` in `pupa_settings.py`, e.g. `postgis://USERNAME:PASSWORD@localhost/pupa`.

## Run a scraper

    pupa update ca_ab_edmonton

To run only the scraping step and skip the import step add the `--scrape` switch:

    pupa update --scrape ca_ab_edmonton

For documentation on the `pupa` command:

    pupa -h

For documentation on the `update` subcommand:

    pupa update -h

## Create a scraper

See the first few steps of [this wiki page](https://github.com/opennorth/represent-canada/wiki/Tasks%3A-Represent-CSV-Schema#3-importing-the-data-into-represent) to create a scraper.

## Develop a scraper

Read the [Open Civic Data documentation](https://open-civic-data-docs.readthedocs.io/en/latest/scrape/) or an existing scraper's code.

Avoid using the XPath `string()` function unless the expression is known to not have matches on some pages. Otherwise, scrapers may continue to run without error despite failing to find a match. A comment like `# can be empty` or `# allow string()` should accompany the use of `string()`.

Use the `get_email` and `get_phone` helpers as much as possible.

In late 2014/early 2015, we disabled some single-jurisdiction scrapers to lower maintenance costs, some of which have been re-enabled, and disabled all [multi-jurisdiction scrapers](https://github.com/opennorth/represent-canada/issues/95), because Pupa didn't support them. The disabled scrapers are in `disabled/`.

We heavily modify Pupa's validations in `patch.py` to be as strict as possible in order to keep data quality high. We subclass Pupa's `Scraper`, `Jurisdiction` and `Person` classes in `utils.py` to reduce code duplication and to correct common data quality issues.

## Maintenance

List the available maintenance tasks:

    invoke -l

Make the code style consistent:

    flake8

Check module names, class names, `classification`, `division_name`, `name` and `url` in `__init.py__` files:

    invoke tidy

Check sources are credited and assertions are made:

    invoke sources_and_assertions

Check jurisdiction URLs (look for `Delete COUNCIL_PAGE` or `Missing COUNCIL_PAGE` instructions):

    invoke council_pages

Update the OCD-IDs:

    curl -O https://raw.githubusercontent.com/opencivicdata/ocd-division-ids/master/identifiers/country-ca.csv

Check whether any non-authoritative CSVs are likely to be stale:

    invoke csv_stale

Check whether any CSV errors can be reported to data publishers:

    invoke csv_error

Scraper code rarely undergoes code review. The focus is on the quality of the data.

## Bugs? Questions?

This repository is on GitHub: [https://github.com/opencivicdata/scrapers-ca](https://github.com/opencivicdata/scrapers-ca), where your contributions, forks, bug reports, feature requests, and feedback are greatly welcomed.

Copyright (c) 2013 Open North Inc., released under the MIT license
