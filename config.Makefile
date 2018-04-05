export PROJECT_NAME = medbox
export FLASK_APP = medbox
export FLASK_DEBUG = 1
HOST = 0.0.0.0
PORT = 19871

# Python env
VENV = $(PWD)/.env
PIP = $(VENV)/bin/pip
PYTHON = $(VENV)/bin/python
FLASK = $(VENV)/bin/flask

URL_TEST = https://test-$(CI_PROJECT_NAME)-$(BRANCH_NAME).kozea.fr/api/webstore/resip_labo/0248
URL_PROD = https://medbox.pharminfo.fr/api/webstore/resip_labo/0248
