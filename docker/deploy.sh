#!/bin/bash
#
# Assuming you have the latest version Docker installed, this script will
# fully create your environment.
#
set -e

docker pull ubuntu:17.10
docker-compose build
docker-compose up -d
