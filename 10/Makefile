VENV := venv
PYTHON := $(VENV)/bin/python3
PIP := $(VENV)/bin/pip
SETUP := $(PYTHON) setup.py
SHAPE := 20000
SHELL := /bin/bash

all: venv activate deps install run clean

venv:
	@echo "============ Create Virtual Environment: ============"
	@echo
	python3 -m venv $(VENV)
activate: venv
	source ./$(VENV)/bin/activate
deps: activate
	@echo
	@echo "============    Install Dependencies:    ============"
	@echo
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
install: deps
	@echo
	@echo "============        Install Setup:       ============"
	@echo
	$(SETUP) install
run: install
	@echo
	@echo "============         Start Tests:        ============"
	@echo
	$(PYTHON) -m unittest cjson_tests.py
	@echo
	@echo "============      Generate JSON file:    ============"
	@echo
	$(PYTHON) json_generator.py $(SHAPE)
	@echo "Created file with JSON strings (count = $(SHAPE))"
	@echo
	@echo "============    Start Test Performance:  ============"
	@echo
	$(PYTHON) perform.py
clean: run
	@echo
	@echo "============           Clean:            ============"
	@echo
	rm -rf build dist *.egg-info __pycache__ venv _trial_temp json_database.txt
