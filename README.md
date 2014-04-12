# Canadian Legislative Scrapers

See [blank-pupa](https://github.com/opennorth/blank-pupa) to install dependencies and get started.

## Run a scraper

    python -m pupa.cli update --nonstrict ca_ab_edmonton

To run only the scraping step and skip the import step into MongoDB add the `--scrape` switch:

    python -m pupa.cli update --nonstrict --scrape ca_ab_edmonton

For documentation on the `pupa.cli` command:

    python -m pupa.cli -h

For documentation on the `update` subcommand:

    python -m pupa.cli update -h

## Create a scraper

Find division identifiers using the [Open Civic Data Division Identifier (OCD-ID) Viewer](http://opennorth.github.io/ocd-id-viewer/) or by browsing the [list of identifiers](https://github.com/opencivicdata/ocd-division-ids/blob/master/identifiers/country-ca.csv). In most cases, a municipality will have a division identifier with a type ID of `csd`. Then, create a scraper with:

    invoke new --division-id ocd-division/country:ca/csd:5915022

This command creates an `__init__.py` file and a stub `people.py` file within a new directory for the scraper. The `__init_.py` file, which describes the jurisdiction, should not require any editing.

Most jurisdictions have a `geographic_code` that corresponds to a [Standard Geographical Classification (SGC) 2011](http://www.statcan.gc.ca/subjects-sujets/standard-norme/sgc-cgt/2011/sgc-cgt-intro-eng.htm) code. Other jurisdictions have a `division_id` that corresponds to an [OCD-ID](https://github.com/opencivicdata/ocd-division-ids).

## Develop a scraper

Read the [Pupa documentation](http://docs.opencivicdata.org/en/latest/scrape/new.html) or an existing scraper's code.

### Troubleshooting

If the `pupa.cli` command raises the error below, ensure that MongoDB is running.

    TypeError: 'ErrorProxy' object is not subscriptable

### Eliminating duplicates

If, while developing your scraper, you created duplicates, you may need to:

1. Run `invoke flush --division-id=JURISDICTION-ID-OR-DIVISION-ID`
1. Run the MongoDB command
1. Run this repository's `pupa.cli` command or [scrapers_ca_app](https://github.com/opennorth/scrapers_ca_app)'s' `cron.py` command

If the duplicates exist in [Represent](http://represent.opennorth.ca/), perform the MongoDB and `cron.py` steps on Heroku and re-import the data into Represent.

## Maintenance

The `tidy.py` script will correct module names, class names, and `jurisdiction_id`, `division_name`, `name` and `url` in `__init.py__` files. It will report any module without an OCD division or with a `name` or `url` that requires manual verification.

    invoke tidy

To check that all sources are credited, run:

    invoke sources

To test [PEP 8](http://www.python.org/dev/peps/pep-0008/) conformance, run:

    pep8 .

To tidy all whitespace, run:

    autopep8 -i -a -r --ignore=E111,E121,E501,W6 .

To print all jurisdiction URLs:

    invoke urls

Periodically, update the metadata about OCD-IDs:

    ruby constants.rb

Scraper code rarely undergoes code review. The focus is on the quality of the data.

## Bugs? Questions?

This repository is on GitHub: [http://github.com/opencivicdata/scrapers-ca](http://github.com/opencivicdata/scrapers-ca), where your contributions, forks, bug reports, feature requests, and feedback are greatly welcomed.

Copyright (c) 2013 Open North Inc., released under the MIT license
