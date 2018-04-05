include config.Makefile
-include config.custom.Makefile

BASEVERSION ?= v1
BASEROOT ?= https://raw.githubusercontent.com/Kozea/MakeCitron/$(BASEVERSION)/
BASENAME := base.Makefile
ifeq ($(MAKELEVEL), 0)
RV := $(shell wget -q -O $(BASENAME) $(BASEROOT)$(BASENAME) || echo 'FAIL')
ifeq (,$(RV))
include $(BASENAME)
else
$(error Unable to download $(BASEROOT)$(BASENAME))
endif
$(info $(INFO))
else
include $(BASENAME)
endif


all: install serve
	$(LOG)

install-python:
	test -d $(VENV) || virtualenv $(VENV)
	# Top model
	$(PIP) install --upgrade --no-cache git+ssh://git@github.com/Kozea/top_model.git#egg=top_model
	# Deps
	$(PIP) install --upgrade --no-cache pip setuptools -e .[test]

install: install-python
	$(LOG)

install-dev:
	$(PIP) install --upgrade devcore

install-db-test:
	$(VENV)/bin/top_model deploy --recreate-and-deploy-test

install-db:
	$(VENV)/bin/top_model deploy --recreate-and-deploy

serve-python:
	$(FLASK) run --with-threads -h $(HOST) -p $(PORT)

serve: serve-python
	$(LOG)

clean:
	rm -fr dist

clean-install: clean
	rm -fr $(VENV)
	rm -fr *.egg-info

check-outdated:
	$(PIP) list --outdated --format=columns

check: check-python check-outdated
	$(LOG)

deploy-test:
	$(LOG)
	@echo "Communicating with Junkrat..."
	@wget --no-verbose --content-on-error -O- --header="Content-Type:application/json" --post-data=$(subst $(newline),,$(JUNKRAT_PARAMETERS)) $(JUNKRAT) | tee $(JUNKRAT_RESPONSE)
	if [[ $$(tail -n1 $(JUNKRAT_RESPONSE)) != "Success" ]]; then exit 9; fi
	wget --no-verbose --content-on-error -O- $(URL_TEST)

deploy-prod:
	$(LOG)
	@echo "Communicating with Junkrat..."
	@wget --no-verbose --content-on-error -O- --header="Content-Type:application/json" --post-data=$(subst $(newline),,$(JUNKRAT_PARAMETERS)) $(JUNKRAT) | tee $(JUNKRAT_RESPONSE)
	if [[ $$(tail -n1 $(JUNKRAT_RESPONSE)) != "Success" ]]; then exit 9; fi
	wget --no-verbose --content-on-error -O- $(URL_PROD)
