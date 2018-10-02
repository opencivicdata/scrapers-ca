# Docker

## Setup

Build the environment:

    docker pull ubuntu:17.10
    docker-compose build
    docker-compose up -d

Setup the database:

    docker-compose exec scrapers-ca service postgresql start
    docker-compose exec scrapers-ca sudo -u postgres createuser root
    docker-compose exec scrapers-ca sudo -u postgres psql -c 'ALTER USER root WITH SUPERUSER;'
    docker-compose exec scrapers-ca sudo -u postgres psql -c "ALTER USER root WITH PASSWORD 'root';"
    docker-compose exec scrapers-ca sudo -u postgres createdb pupa
    docker-compose exec scrapers-ca sudo -u postgres psql pupa -c "CREATE EXTENSION postgis;"

Modify `pupa_settings.py`:

    docker-compose exec scrapers-ca sed -i -e 's/localhost/root:root@localhost/' /src/scrapers-ca/pupa_settings.py

Open a shell:

    docker-compose exec scrapers-ca /bin/bash
    cd scrapers-ca

Setup the application:

    mkvirtualenv scrapers-ca --python=`which python3`
    pip install -r requirements.txt
    pupa dbinit ca

## Usage

To run a scraper, e.g. `ca_on_candidates`, open a shell as above, and:

    pupa update ca_on_candidates

To wipe the database:

    docker-compose exec scrapers-ca sudo -u postgres dropdb pupa
    docker-compose exec scrapers-ca sudo -u postgres createdb pupa

Then, open a shell as above, and:

    pupa dbinit ca
