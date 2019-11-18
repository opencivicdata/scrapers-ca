#!/bin/bash
#
# Set up a Docker environment.
#
set -e

echo "Setting up a Docker environment."

docker-compose build --pull
docker-compose up -d

echo ""
echo "Starting postgresql."
docker-compose exec scrapers-ca service postgresql start

echo ""
echo "Trying to create user root."
docker-compose exec scrapers-ca sudo -u postgres createuser root || ALREADYEXISTS="EXISTS"
if [ "$ALREADYEXISTS" == "EXISTS" ]; then
  echo ""
  echo 'We got an error when trying to create user root; we will'
  echo 'assume that that is because the script was already called and'
  echo 'everything is already set up; moving on...'
else
  echo ""
  echo "User root has been created, make it a superuser and set its password,"
  echo "then set up the application, which can take several minutes."
  docker-compose exec scrapers-ca sudo -u postgres psql -c 'ALTER USER root WITH SUPERUSER;'
  docker-compose exec scrapers-ca sudo -u postgres psql -c "ALTER USER root WITH PASSWORD 'root';"
  docker-compose exec scrapers-ca sudo -u postgres createdb pupa
  docker-compose exec scrapers-ca sudo -u postgres psql pupa -c "CREATE EXTENSION postgis;"
  echo ""
  echo "Modifying pupa_settings.py with root:root if it has not yet"
  echo "been modified. Note that this will modify the file on your"
  echo "host computer because it is shared between the host and the"
  echo "container."
  docker-compose exec scrapers-ca sed -i -e 's/\/\/localhost/\/\/root:root@localhost/g' /src/scrapers-ca/pupa_settings.py
  echo ""
  echo "Set up the application"
  docker-compose exec scrapers-ca /bin/bash -i -c '
  pip3 install -r requirements.txt && \
  pupa dbinit ca'
fi

echo ""
echo "Everything seems up and running."
echo ""
echo "Please refer to ./docker/README.md for usage."
echo ""
