VENV := venv
PYTHON := python3
PIP := $(VENV)/bin/pip
SETUP := $(PYTHON) setup.py
SHAPE := 20000

all: venv deps install run clean

venv:
	@echo "\n============ Create Virtual Environment: ============\n"
	$(PYTHON) -m venv $(VENV)
	$(PIP) install --upgrade pip
deps:
	@echo "\n============    Install Dependencies:    ============\n"
	$(PIP) install -r requirements.txt
install:
	@echo "\n============        Install Setup:       ============\n"
	$(SETUP) install
run:
	@echo "\n============         Start Tests:        ============\n"
	$(PYTHON) -m unittest cjson_tests.py
	@echo "\n============      Generate JSON file:    ============\n"
	$(PYTHON) json_generator.py $(SHAPE)
	@echo "Created file with JSON strings (count = $(SHAPE))"
	@echo "\n============    Start Test Performance:  ============\n"
	$(PYTHON) perform.py
clean:
	@echo "\n============           Clean:            ============\n"
	rm -rf build dist *.egg-info __pycache__ venv _trial_temp json_database.txt
