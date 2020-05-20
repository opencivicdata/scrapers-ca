FROM ubuntu:18.04

ENV DEBIAN_FRONTEND=noninteractive

# Base setup
RUN apt-get -y update
# PostgreSQL
RUN apt-get -y install postgresql libpq-dev postgresql-client postgresql-client-common gdal-bin postgresql-contrib postgis
# Python
RUN apt-get -y install python3 python3-pip python3-dev build-essential python3-invoke python3-lxml python3-unidecode python3-regex libxml2-dev libxslt-dev lib32z1-dev git sudo
RUN apt-get clean
RUN pip3 install virtualenv virtualenvwrapper ndg_httpsclient flake8

# .bashrc
RUN echo 'export WORKON_HOME=$HOME/.virtualenvs' >> $HOME/.bashrc
RUN echo 'export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3.6' >> $HOME/.bashrc
RUN echo 'export PROJECT_HOME=/src/scrapers-ca' >> $HOME/.bashrc
RUN echo 'source /usr/local/bin/virtualenvwrapper.sh' >> $HOME/.bashrc

RUN mkdir /src

WORKDIR /src/scrapers-ca
