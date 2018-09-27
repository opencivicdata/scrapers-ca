#!/bin/bash
#
# Assuming you have the latest version Docker installed, this script will
# fully create your environment.
#
set -e

docker pull ubuntu:17.10
docker-compose build
docker-compose up -d

docker-compose exec scrapers-ca service postgresql start
docker-compose exec scrapers-ca sudo -u postgres createuser root
docker-compose exec scrapers-ca sudo -u postgres psql -c 'ALTER USER root WITH SUPERUSER;'
docker-compose exec scrapers-ca sudo -u postgres psql -c "ALTER USER root WITH PASSWORD 'root';"
docker-compose exec scrapers-ca sudo -u postgres createdb pupa
docker-compose exec scrapers-ca sudo -u postgres psql pupa -c "CREATE EXTENSION postgis;"
docker-compose exec scrapers-ca sed -i -e 's/localhost/root:root@localhost/' /src/scrapers-ca/pupa_settings.py
