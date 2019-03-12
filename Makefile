SHELL := /bin/bash

FUNCTION=s3_trigger_goobi
PY_VERSION=python3.5

.PHONY: zip
all: zip

.PHONY: clean
clean:
	rm -rf venv
	rm -f ${FUNCTION}.zip

venv:
	virtualenv -p ${PY_VERSION} venv

.PHONY: dependencies
dependencies: venv
	source venv/bin/activate; pip install -r requirements.txt

zip: venv dependencies
	cd venv/lib/${PY_VERSION}/site-packages/; zip -r9 ../../../../${FUNCTION}.zip .
	zip -g ${FUNCTION}.zip ${FUNCTION}.py
