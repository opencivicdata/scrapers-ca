# Canadian Legislative Scrapers

## Installation

Follow the instructions in the [Python Quick Start Guide](https://github.com/opennorth/opennorth.ca/wiki/Python-Quick-Start%3A-OS-X) to install Homebrew, Git, MongoDB, Python and virtualenv. You must use Python 2.7. You may need to force virtualenv to use your Python 2.7 executable by running, for example, `export VIRTUALENV_PYTHON=/usr/bin/python`.

```
mkvirtualenv scrapers-ca
git clone git://github.com/opencivicdata/scrapers-ca.git
cd scrapers-ca
pip install -r requirements.txt
```

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

## Maintenance

The `tidy` task will correct module names, class names, and `jurisdiction_id`, `division_name`, `name` and `url` in `__init.py__` files. It will report any module without an OCD division or with a `name` or `url` that requires manual verification.

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
