#!/bin/bash

set -e

docker-compose exec scrapers-ca sudo -u postgres dropdb pupa
docker-compose exec scrapers-ca sudo -u postgres createdb pupa
