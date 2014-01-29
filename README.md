# Canadian Legislative Scrapers

See [blank-pupa](https://github.com/opennorth/blank-pupa) to install dependencies and get started.

## Run a scraper

```
python -m pupa.cli update ca_ab_edmonton
```

## Geographic codes

Most jurisdictions have a `geographic_code` that corresponds to the [Standard Geographical Classification (SGC) 2011](http://www.statcan.gc.ca/subjects-sujets/standard-norme/sgc-cgt/2011/sgc-cgt-intro-eng.htm) geographic code. Other jurisdictions have an `division_id` that corresponds to the [Open Civic Data Division Identifier](https://github.com/opencivicdata/ocd-division-ids).

## Maintenance

The `tasks.py` script will correct module names, class names, and `jurisdiction_id`, `division_name`, `name` and `url` in `__init.py__` files. It will report any module without an OCD division or with a `name` or `url` that requires manual verification.

    python tasks.py

To test [PEP 8](http://www.python.org/dev/peps/pep-0008/) conformance, run:

    pep8 .

To tidy all whitespace, run:

    autopep8 -i -a -r --ignore=E111,E121,E501,W6 .

Scraper code rarely undergoes code review. The focus is on the quality of the data.

## Bugs? Questions?

This repository is on GitHub: [http://github.com/opencivicdata/scrapers-ca](http://github.com/opencivicdata/scrapers-ca), where your contributions, forks, bug reports, feature requests, and feedback are greatly welcomed.

Copyright (c) 2013 Open North Inc., released under the MIT license
