#
# Run deploy.sh to build a scrapers-ca Docker development environment.
#

# Commands:
./deploy.sh
# ssh into the Docker environment:
./shell.sh
cd scrapers-ca
mkvirtualenv scrapers-ca --python=`which python3`
pip install -r requirements.txt
pupa dbinit ca
# You can now run your scraper. Ex: pupa update ca_on_candidates

# To wipe the database:
./db-refresh.sh
./shell.sh
pupa dbinit ca

# Alter pupa_settings
docker-compose exec scrapers-ca sed -i -e 's/localhost/root:root@localhost/' /src/scrapers-ca/pupa_settings.py
