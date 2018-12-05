FROM ubuntu:17.10

# Base setup
RUN apt-get -y update
RUN apt-get -y install postgresql libpq-dev postgresql-client postgresql-client-common gdal-bin postgresql-9.6-postgis-scripts  python3 python3-pip python3-dev build-essential python3-invoke python3-lxml python3-unidecode python3-regex libxml2-dev libxslt-dev lib32z1-dev git sudo
RUN apt-get clean
RUN pip3 install virtualenv virtualenvwrapper ndg_httpsclient tidy flake8

# .bashrc
RUN echo 'export WORKON_HOME=$HOME/.virtualenvs' >> $HOME/.bashrc
RUN echo 'export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3.6' >> $HOME/.bashrc
RUN echo 'export PROJECT_HOME=/src/scrapers-ca' >> $HOME/.bashrc
RUN echo 'source /usr/local/bin/virtualenvwrapper.sh' >> $HOME/.bashrc

RUN mkdir /src

WORKDIR /src/scrapers-ca
