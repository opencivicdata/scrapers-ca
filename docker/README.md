# Docker

## Setup

    cd ./docker && ./deploy.sh

The first time you run ./deploy.sh, it might take several minutes, but will take a few seconds on future runs.

## Destroying the environment

    docker-compose down

## Opening a shell

Once Docker is set up (deployed), open a shell like this:

    cd ./docker && docker-compose exec scrapers-ca /bin/bash

## Usage

To run a scraper, e.g. `ca_on`, open a shell as above, and:

    pupa update ca_on

To wipe the database:

    docker-compose exec scrapers-ca sudo -u postgres dropdb pupa
    docker-compose exec scrapers-ca sudo -u postgres createdb pupa

Then, open a shell as above, and:

    pupa dbinit ca

To interact with the postgres db directly for debugging purposes:

    psql pupa root


