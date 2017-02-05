# Canadian Legislative Scrapers [![Build Status](https://travis-ci.org/opencivicdata/scrapers-ca.png?branch=master)](https://travis-ci.org/opencivicdata/scrapers-ca)

## Usage

Follow the instructions in the [Python Quick Start Guide](https://github.com/opennorth/wiki/wiki/Python-Quick-Start%3A-OS-X) to install Homebrew, Git, PostGIS, Python 3.3+ and virtualenv.

```
mkvirtualenv scrapers-ca --python=`which python3`
git clone git://github.com/opencivicdata/scrapers-ca.git
cd scrapers-ca
pip install -r requirements.txt
```

Initialize the database:

```
createdb pupa
psql pupa -c "CREATE EXTENSION postgis;"
pupa dbinit ca
```

## Run a scraper

    pupa update ca_ab_edmonton

To run only the scraping step and skip the import step add the `--scrape` switch:

    pupa update --scrape ca_ab_edmonton

For documentation on the `pupa` command:

    pupa -h

For documentation on the `update` subcommand:

    pupa update -h

## Create a scraper

Find division identifiers using the [Open Civic Data Division Identifier (OCD-ID) Viewer](https://opencivicdata.github.io/ocd-id-viewer/) or by browsing the [list of identifiers](https://github.com/opencivicdata/ocd-division-ids/blob/master/identifiers/country-ca.csv). In most cases, a municipality will have a division identifier with a type ID of `csd`. Create a scraper with:

    pupa init ca_on_toronto

## Develop a scraper

Read the [Pupa documentation](http://docs.opencivicdata.org/en/latest/scrape/basics.html) or an existing scraper's code.

Avoid using the XPath `string()` function unless the expression is known to not have matches on some pages. Otherwise, scrapers may continue to run without error despite failing to find a match. A comment like `# can be empty` or `# allow string()` should accompany the use of `string()`.

Use the `get_email` and `get_phone` helpers as much as possible.

In late 2014/early 2015, we disabled some single-jurisdiction scrapers to lower maintenance costs, some of which have been re-enabled, and disabled all [multi-jurisdiction scrapers](https://github.com/opennorth/represent-canada/issues/95), because Pupa didn't support them. The disabled scrapers are in `disabled/`.

## Maintenance

Make the code style consistent:

    flake8

Check module names, class names, `classification`, `division_name`, `name` and `url` in `__init.py__` files:

    invoke tidy

Check sources are credited and assertions are made:

    invoke sources_and_assertions

Check jurisdiction URLs:

    invoke urls

Update the OCD-IDs:

    curl -O https://raw.githubusercontent.com/opencivicdata/ocd-division-ids/master/identifiers/country-ca.csv

Scraper code rarely undergoes code review. The focus is on the quality of the data.

## Bugs? Questions?

This repository is on GitHub: [https://github.com/opencivicdata/scrapers-ca](https://github.com/opencivicdata/scrapers-ca), where your contributions, forks, bug reports, feature requests, and feedback are greatly welcomed.

Copyright (c) 2013 Open North Inc., released under the MIT license
