include Makefile.config
-include Makefile.custom.config

all: install serve

install-python:
	test -d $(VENV) || virtualenv $(VENV)
	# Top model
	$(PIP) install --upgrade --no-cache git+ssh://git@github.com/Kozea/top_model.git#egg=top_model
	# Deps
	$(PIP) install --upgrade --no-cache pip setuptools -e .[test]

install: install-python

install-dev:
	$(PIP) install --upgrade devcore

install-db-test:
	$(VENV)/bin/top_model deploy --recreate-and-deploy-test

install-db:
	$(VENV)/bin/top_model deploy --recreate-and-deploy

serve-python:
	$(FLASK) run --with-threads -h $(HOST) -p $(PORT)

serve: serve-python

clean:
	rm -fr dist

clean-install: clean
	rm -fr $(VENV)
	rm -fr *.egg-info

check-outdated:
	$(PIP) list --outdated --format=columns

check: check-python check-outdated
