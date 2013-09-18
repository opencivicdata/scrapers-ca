## Pupa Scrapers for Canada

See [blank-pupa](https://github.com/opennorth/blank-pupa) to install dependencies and get started.

## Geographic codes

Most jurisdictions have a `geographic_code` that corresponds to its [Standard Geographical Classification (SGC) 2011](http://www.statcan.gc.ca/subjects-sujets/standard-norme/sgc-cgt/2011/sgc-cgt-intro-eng.htm) geographic code.

Other jurisdictions have an `ocd_division` that corresponds to its [Open Civic Data Division Identifier](https://github.com/opencivicdata/ocd-division-ids).

## Maintenance

The `tasks.py` script will correct module names, class names, and `jurisdiction_id`, `name`, `legislature_name` and `legislature_url` in `__init.py__` files. It will report any module without an OCD division or with a `legislature_name` or `legislature_url` that requires manual verification.

    python tasks.py

To test [PEP 8](http://www.python.org/dev/peps/pep-0008/) conformance, run:

    pep8 .

To tidy all whitespace, run:

    autopep8 -i -a -r --ignore=E111,E121,E501,W6 .

## Bugs? Questions?

This repository is on GitHub: [http://github.com/opencivicdata/scrapers-ca](http://github.com/opencivicdata/scrapers-ca), where your contributions, forks, bug reports, feature requests, and feedback are greatly welcomed.

Copyright (c) 2013 Open North Inc., released under the MIT license
